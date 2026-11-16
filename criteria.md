## 1. Burstiness Signal Calculation
**Target:** For every valid submission, the Burstiness Signal must produce a finite score between `0` and `1`, calculated using the normalization formula `B = 1 / (1 + V)`, where `V` is the population variance of GPT-2's per-token prediction losses. When tested with controlled per-token loss values, the calculated variance and normalized score must match the independently calculated expected results within a tolerance of `0.000001`.

**How I verify it:** I test the calculation using controlled per-token loss values with known population variances. For example, loss values `[0, 2]` have a population variance of `1`, which should produce a Burstiness Score of `0.5`. I also test equal loss values, which should produce a variance of `0` and a score of `1`. I compare the implementation's results against these expected values.

**Why this matters:** The new signal is based on prediction-loss variance, so verifying its calculation is essential before evaluating whether it provides useful information. The score is normalized to the `[0, 1]` range, making this a clear boundary. The small tolerance accounts for floating-point precision without allowing meaningful calculation errors.

## 2. Integration Into the Weighted Scoring System
**Target:** Every successful submission must return and log the Burstiness Signal alongside the Model and Style Signals. The combined score must match the formula `0.50M + 0.25B + 0.25T` within a tolerance of `0.000001`, using the configured weights.

**How I verify it:** I submit samples from `scenarios.py`, inspect the returned scores, and compare each combined score against an independently calculated result using the three individual signals and configured weights. I also inspect the corresponding audit entries to confirm that the Burstiness Score is recorded.

**Why this matters:** The extension must contribute to the existing detection system rather than operate independently. The weights are intentionally fixed during baseline evaluation, and a strict tolerance verifies that the new signal is incorporated correctly without silently changing the existing scoring behavior.

## 3. Computational Overhead
**Target:** The extension must reuse the existing GPT-2 inference pass without performing a second model inference. After the model has loaded, the average `/submit` processing time across 20 successful submissions from `scenarios.py` must not exceed `600 ms`, measured using `time.perf_counter()` on the same local CPU environment.

**How I verify it:** I inspect the `model_signals` implementation and instrument the GPT-2 model forward call to confirm that a successful submission performs exactly one model inference pass for both the Model and Burstiness Signals. I then submit all 20 samples from `scenarios.py`, record the `duration_ms` values from the audit log, and calculate their average. I allow approximately seven seconds between submissions to stay below the existing rate limit.

**Why this matters:** Reusing the existing inference pass was an explicit design constraint. The initial ten-run baseline averaged `452.81 ms`, so a `600 ms` limit allows approximately 32% additional processing time while keeping the extension within a reasonable performance range. Initial model download and loading are excluded because they are one-time startup costs rather than normal per-submission processing.

## 4. Burstiness Signal's Ability to Distinguish Sample Types
**Target:** Across the 10 human-written and 10 AI-generated samples in `scenarios.py`, the average Burstiness Score for AI-generated samples must be at least `0.01` higher than the average for human-written samples. The same predefined samples must be used without modification during the evaluation.

**How I verify it:** I submit all 20 samples from `scenarios.py`, keeping their expected sample types separate. I retrieve their individual Burstiness Scores from the audit log, calculate the average for each category, and subtract the human average from the AI average. I compare the difference against the `0.01` target.

**Why this matters:** The Burstiness Signal is intended to provide information that helps distinguish the two sample types. In the initial baseline of five samples per category, the AI average was approximately `0.1223`, compared with `0.1026` for human samples, a difference of approximately `0.0198`. A `0.01` minimum preserves a meaningful directional difference while allowing some variation in subsequent testing. This small sample is an exploratory check, not statistical proof of detection accuracy.

## 5. Classification Outcomes
**Target:** Across all 20 samples in `scenarios.py` (10 human-written and 10 AI-generated):

- Zero human-written samples may receive the `ai` label.
- At least 1 out of 10 AI-generated samples must receive the `ai` label.
The labels are determined by the classification thresholds in `config.py`. The same predefined samples must be used without modification throughout the evaluation.

**How I verify it:** I submit all 20 samples from `scenarios.py`, alternating between human-written and AI-generated samples. I record the expected sample type and returned classification for each submission. I then count the number of human samples classified as `ai` and the number of AI samples classified as `ai`. I compare both counts against the targets.

**Why this matters:** A false positive can incorrectly accuse a human writer of using AI, so I set a strict target of zero human samples receiving the `ai` label. At the same time, requiring at least one AI sample to receive the `ai` label ensures that the system can identify at least some AI-generated content rather than classifying every submission as `unsure` or `human`. This is an initial minimum target, not a claim of high classification accuracy.