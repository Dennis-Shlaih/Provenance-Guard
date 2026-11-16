# Provenance Guard reproducible criterion tests

These scripts use the existing `HUMAN_SAMPLES` and `AI_SAMPLES` in the project-root
`scenarios.py`, and the `/submit`, `/health`, and `/log` routes in `app.py`.

## Files

- `test_criterion_1.py` — checks the actual `model_metrics()` variance calculation using controlled synthetic token losses, then verifies that empty,
  missing, and too-short text submissions receive HTTP 400 responses and audit
  rejection entries. Runs the API invalid-input cases three times.
- `test_criterion_3.py` — instruments the loaded detector model and verifies that
  `detector.model_signals()` makes exactly one GPT-2 `forward()` call. Runs three
  checks.
- `run_criteria_2_4_5.py` — sends the same 10 human and 10 AI samples in three
  trials. It checks the weighted score, server-side average latency, burstiness
  separation, and classification outcomes. It writes detailed JSON results to
  `tests/criteria_2_4_5_results.json`.

## How to run

1. Put the `tests` folder in the same project root as `app.py`, `detector.py`,
   `config.py`, and `scenarios.py`.
2. Install the project's pinned dependencies and activate its virtual environment.
3. Start the service in Terminal 1:

   ```bash
   python app.py
   ```

4. In Terminal 2, from the project root, run:

   ```bash
   python tests/test_criterion_1.py
   python tests/test_criterion_3.py
   python tests/run_criteria_2_4_5.py
   ```

The 20-sample evaluation sends 60 requests over three trials. If rate limiting is
enabled at 10 requests/minute, it takes about six minutes. Run the scripts when
the service is otherwise idle so unrelated requests do not affect the rate limit.

## Important interpretation

A PASS means the stated operational criterion was met on these fixed samples and
this machine. It does not establish that the detector is generally accurate or
that burstiness is a reliable authorship signal. Preserve the JSON output and
record the environment and date with the evaluation results.
