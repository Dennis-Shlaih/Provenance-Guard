#!/usr/bin/env python3
"""Criterion 1: burstiness calculation and invalid-input handling.

Run from the project root:
    python tests/test_criterion_1.py
The Flask app must already be running.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import detector  # noqa: E402

BASE_URL = "http://127.0.0.1:5000"
TRIALS = 3
TIMEOUT_SECONDS = 30


def request_json(path: str, payload: dict | None = None):
    data = json.dumps(payload).encode("utf-8")
    request = Request(
        BASE_URL + path,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"raw_body": body}
        return exc.code, parsed
    except URLError as exc:
        raise RuntimeError(f"Could not reach {BASE_URL}. Is app.py running?") from exc


def get_json(path: str):
    request = Request(BASE_URL + path, method="GET")
    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def check_burstiness_math():
    import torch

    # Feed model_metrics two deliberately controlled token losses: approximately
    # 0 and exactly 2. Their population variance is approximately 1.
    class FakeTokenizer:
        def __call__(self, text, **kwargs):
            return {"input_ids": torch.tensor([[0, 1, 0]], dtype=torch.long)}

    class FakeModel:
        def __call__(self, input_ids):
            logits = torch.zeros((1, 3, 2), dtype=torch.float32)
            logits[0, 0, 0] = -100.0  # target at position 0 is token 1: loss ~0
            logits[0, 0, 1] = 0.0
            logits[0, 1, 0] = 0.0    # target at position 1 is token 0: loss = 2
            logits[0, 1, 1] = math.log(math.expm1(2.0))
            return SimpleNamespace(logits=logits)

    original_load = detector._load
    detector._load = lambda: (FakeModel(), FakeTokenizer())
    try:
        perplexity, actual_variance = detector.model_metrics("controlled test text")
        actual_score = detector.burstiness_score_from_variance(actual_variance)

        assert math.isfinite(perplexity)
        assert math.isclose(actual_variance, 1.0, abs_tol=1e-5), (
            f"Expected population variance approximately 1.0, got {actual_variance}"
        )
        assert math.isfinite(actual_score)
        assert 0.0 <= actual_score <= 1.0
        assert math.isclose(actual_score, 0.5, abs_tol=1e-5)
        print(
            "PASS controlled token-loss calculation: "
            f"variance={actual_variance:.6f}, burstiness_score={actual_score:.4f}"
        )

        # Also verify the two simple boundary cases for the variance-to-score mapping.
        zero_variance_score = detector.burstiness_score_from_variance(0.0)
        assert math.isclose(zero_variance_score, 1.0, abs_tol=1e-6)
        print("PASS mapping boundary: variance=0 -> burstiness_score=1.0000")
    finally:
        detector._load = original_load


def main():
    print("Criterion 1 — burstiness calculation and invalid inputs")
    check_burstiness_math()

    health = get_json("/health")
    rate_limiting = bool(health.get("rate_limiting"))
    interval = 60.2 / 10 if rate_limiting else 0.0
    print(f"Rate limiting enabled: {rate_limiting}")

    # Each case should be rejected by /submit with HTTP 400 and leave an audit entry.
    for trial in range(1, TRIALS + 1):
        cases = [
            {
                "name": "empty text",
                "payload": {"text": "", "creator_id": f"c1_empty_{trial}"},
                "creator_id": f"c1_empty_{trial}",
                "reason": "missing_or_invalid_text",
            },
            {
                "name": "missing text",
                "payload": {"creator_id": f"c1_missing_{trial}"},
                "creator_id": f"c1_missing_{trial}",
                "reason": "missing_or_invalid_text",
            },
            {
                "name": "too-short text",
                "payload": {"text": "Hi", "creator_id": f"c1_short_{trial}"},
                "creator_id": f"c1_short_{trial}",
                "reason": "text_too_short",
            },
        ]

        for index, case in enumerate(cases):
            status, body = request_json("/submit", case["payload"])
            assert status == 400, (
                f"FAIL trial {trial}, {case['name']}: expected HTTP 400, "
                f"got {status}: {body}"
            )
            assert "error" in body, (
                f"FAIL trial {trial}, {case['name']}: response has no error field: {body}"
            )
            print(f"PASS trial {trial} — {case['name']}: HTTP {status}")

            if rate_limiting and not (
                trial == TRIALS and index == len(cases) - 1
            ):
                time.sleep(interval)

        log_data = get_json("/log?limit=1000")
        entries = log_data.get("entries", [])
        for case in cases:
            matching = [
                entry for entry in entries
                if entry.get("creator_id") == case["creator_id"]
                and entry.get("reason") == case["reason"]
            ]
            assert matching, (
                f"FAIL trial {trial}: no audit rejection found for "
                f"{case['name']} ({case['creator_id']})"
            )
            print(f"PASS trial {trial} — {case['name']} recorded in audit log")

    print("\nCriterion 1: PASS")


if __name__ == "__main__":
    main()
