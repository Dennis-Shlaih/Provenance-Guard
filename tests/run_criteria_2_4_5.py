#!/usr/bin/env python3
"""Criteria 2, 3 (latency), 4, and 5: 20-sample API evaluation.

Run from the project root while app.py is running:
    python tests/run_criteria_2_4_5.py

This sends the same 10 human and 10 AI samples in three trials. It checks:
- Criterion 2: returned combined score matches the weighted formula.
- Criterion 3: mean server-side /submit duration is <= 600 ms per trial.
- Criterion 4: mean AI burstiness is at least 0.01 above mean human burstiness.
- Criterion 5: zero human samples are labelled "ai", and >=1 AI sample is "ai".

The script respects the configured 10/minute limit by spacing requests.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
from scenarios import AI_SAMPLES, HUMAN_SAMPLES  # noqa: E402

BASE_URL = "http://127.0.0.1:5000"
TRIALS = 3
LATENCY_LIMIT_MS = 600.0
BURSTINESS_GAP = 0.01
TIMEOUT_SECONDS = 60
RESULTS_PATH = ROOT / "tests" / "criteria_2_4_5_results.json"


def get_json(path: str):
    request = Request(BASE_URL + path, method="GET")
    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(path: str, payload: dict):
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


def interleave_samples():
    samples = []
    for index, (human_text, ai_text) in enumerate(zip(HUMAN_SAMPLES, AI_SAMPLES), 1):
        samples.append({"sample_type": "human", "sample_number": index, "text": human_text})
        samples.append({"sample_type": "ai", "sample_number": index, "text": ai_text})
    return samples


def audit_entries_for(content_ids: set[str]):
    data = get_json("/log?limit=1000")
    return {
        entry.get("content_id"): entry
        for entry in data.get("entries", [])
        if entry.get("content_id") in content_ids
    }


def main():
    if len(HUMAN_SAMPLES) != 10 or len(AI_SAMPLES) != 10:
        raise AssertionError(
            "Expected exactly 10 HUMAN_SAMPLES and 10 AI_SAMPLES in scenarios.py."
        )

    health = get_json("/health")
    rate_limiting = bool(health.get("rate_limiting"))
    per_minute = int(getattr(config, "RATE_LIMIT_PER_MINUTE", 10))
    interval = (60.2 / per_minute) if rate_limiting else 0.0

    print("Criteria 2, 3, 4, and 5 — three 20-sample trials")
    print(f"Rate limiting enabled: {rate_limiting}; request interval: {interval:.2f}s")
    print("The same 20 texts will be used unchanged in every trial.\n")

    all_trials = []
    next_request_time = time.monotonic()

    for trial in range(1, TRIALS + 1):
        print(f"--- Trial {trial}/{TRIALS} ---")
        trial_results = []
        content_ids = set()

        for sample_index, sample in enumerate(interleave_samples(), 1):
            if interval:
                wait = next_request_time - time.monotonic()
                if wait > 0:
                    time.sleep(wait)

            creator_id = "criteria_eval_shared"  # one key so the per-creator limiter is exercised
            status, body = post_json(
                "/submit",
                {"text": sample["text"], "creator_id": creator_id},
            )
            next_request_time = time.monotonic() + interval

            if status != 200:
                raise AssertionError(
                    f"Trial {trial}, sample {sample_index}: expected HTTP 200, "
                    f"got {status}: {body}"
                )

            required = (
                "content_id",
                "guess",
                "model_score",
                "burstiness_score",
                "style_score",
                "combined_score",
            )
            missing = [key for key in required if key not in body]
            if missing:
                raise AssertionError(
                    f"Trial {trial}, sample {sample_index}: response missing {missing}"
                )

            model_score = float(body["model_score"])
            burstiness_score = float(body["burstiness_score"])
            style_score = float(body["style_score"])
            combined_score = float(body["combined_score"])
            expected_score = round(
                0.50 * model_score + 0.25 * burstiness_score + 0.25 * style_score,
                4,
            )
            score_match = math.isclose(
                combined_score, expected_score, rel_tol=0.0, abs_tol=1e-6
            )
            if not score_match:
                raise AssertionError(
                    f"Criterion 2 failed in trial {trial}, sample {sample_index}: "
                    f"combined={combined_score}, expected={expected_score}"
                )

            content_id = body["content_id"]
            content_ids.add(content_id)
            trial_results.append({
                "sample_type": sample["sample_type"],
                "sample_number": sample["sample_number"],
                "creator_id": creator_id,
                "content_id": content_id,
                "http_status": status,
                "model_score": model_score,
                "burstiness_score": burstiness_score,
                "style_score": style_score,
                "combined_score": combined_score,
                "expected_combined_score": expected_score,
                "guess": body["guess"],
            })
            print(
                f"{sample_index:02d}/20 {sample['sample_type']:5s} "
                f"B={burstiness_score:.4f} combined={combined_score:.4f} "
                f"guess={body['guess']}"
            )

        # Read server-side processing durations from the audit log.
        logged = audit_entries_for(content_ids)
        missing_durations = content_ids - {
            cid for cid, entry in logged.items() if entry.get("duration_ms") is not None
        }
        if missing_durations:
            raise AssertionError(
                f"Trial {trial}: missing audit duration for {len(missing_durations)} "
                "successful submissions."
            )

        for result in trial_results:
            entry = logged[result["content_id"]]
            result["duration_ms"] = float(entry["duration_ms"])

        human_burstiness = [
            row["burstiness_score"] for row in trial_results
            if row["sample_type"] == "human"
        ]
        ai_burstiness = [
            row["burstiness_score"] for row in trial_results
            if row["sample_type"] == "ai"
        ]
        human_mean = sum(human_burstiness) / len(human_burstiness)
        ai_mean = sum(ai_burstiness) / len(ai_burstiness)
        burstiness_gap = ai_mean - human_mean

        durations = [row["duration_ms"] for row in trial_results]
        average_duration = sum(durations) / len(durations)

        human_ai_labels = [
            row for row in trial_results
            if row["sample_type"] == "human" and row["guess"] == "ai"
        ]
        ai_ai_labels = [
            row for row in trial_results
            if row["sample_type"] == "ai" and row["guess"] == "ai"
        ]

        metrics = {
            "trial": trial,
            "sample_count": len(trial_results),
            "criterion_2_all_scores_match": True,
            "criterion_3_average_duration_ms": round(average_duration, 2),
            "criterion_3_pass": average_duration <= LATENCY_LIMIT_MS,
            "criterion_4_human_mean_burstiness": round(human_mean, 6),
            "criterion_4_ai_mean_burstiness": round(ai_mean, 6),
            "criterion_4_gap": round(burstiness_gap, 6),
            "criterion_4_pass": burstiness_gap >= BURSTINESS_GAP,
            "criterion_5_human_ai_labels": len(human_ai_labels),
            "criterion_5_ai_samples_labelled_ai": len(ai_ai_labels),
            "criterion_5_pass": (
                len(human_ai_labels) == 0 and len(ai_ai_labels) >= 1
            ),
            "samples": trial_results,
        }
        all_trials.append(metrics)

        print(f"\nTrial {trial} summary:")
        print(f"  Criterion 2 weighted-score formula: PASS")
        print(
            f"  Criterion 3 mean server duration: {average_duration:.2f} ms "
            f"(limit {LATENCY_LIMIT_MS:.0f} ms) — "
            f"{'PASS' if metrics['criterion_3_pass'] else 'FAIL'}"
        )
        print(
            f"  Criterion 4 mean burstiness: human={human_mean:.4f}, "
            f"AI={ai_mean:.4f}, gap={burstiness_gap:.4f} "
            f"(required >= {BURSTINESS_GAP:.2f}) — "
            f"{'PASS' if metrics['criterion_4_pass'] else 'FAIL'}"
        )
        print(
            f"  Criterion 5 labels: human→AI={len(human_ai_labels)}, "
            f"AI→AI={len(ai_ai_labels)} — "
            f"{'PASS' if metrics['criterion_5_pass'] else 'FAIL'}\n"
        )

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(all_trials, indent=2), encoding="utf-8")

    criteria_pass = {
        "criterion_2": all(t["criterion_2_all_scores_match"] for t in all_trials),
        "criterion_3": all(t["criterion_3_pass"] for t in all_trials),
        "criterion_4": all(t["criterion_4_pass"] for t in all_trials),
        "criterion_5": all(t["criterion_5_pass"] for t in all_trials),
    }
    print("Overall results across all three trials:")
    for criterion, passed in criteria_pass.items():
        print(f"  {criterion}: {'PASS' if passed else 'FAIL'}")
    print(f"\nDetailed results saved to: {RESULTS_PATH}")

    if not all(criteria_pass.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
