#!/usr/bin/env python3
"""Criterion 3: confirm model and burstiness signals share one GPT-2 forward pass.

Run from the project root:
    python tests/test_criterion_3.py

The first run may download the configured model. This test calls the detector
directly; the Flask app does not need to be running.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import detector  # noqa: E402
from scenarios import HUMAN_SAMPLES  # noqa: E402

TRIALS = 3


def main():
    print("Criterion 3 — one GPT-2 forward pass for both model signals")
    detector.warm_up()

    model = detector._model
    if model is None:
        raise RuntimeError("Detector did not load its model.")

    original_forward = model.forward

    for trial in range(1, TRIALS + 1):
        call_count = 0

        def counted_forward(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return original_forward(*args, **kwargs)

        model.forward = counted_forward
        try:
            model_score, burstiness_score = detector.model_signals(HUMAN_SAMPLES[0])
        finally:
            model.forward = original_forward

        assert call_count == 1, (
            f"Trial {trial}: expected exactly one model.forward call, "
            f"observed {call_count}"
        )
        assert 0.0 <= model_score <= 1.0
        assert 0.0 <= burstiness_score <= 1.0
        print(
            f"PASS trial {trial}: forward_calls={call_count}, "
            f"model_score={model_score:.4f}, "
            f"burstiness_score={burstiness_score:.4f}"
        )

    print("\nCriterion 3 one-pass check: PASS")
    print("Note: API processing latency is measured by run_criteria_2_4_5.py.")


if __name__ == "__main__":
    main()
