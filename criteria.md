## 1. False positives on human writing

**Target:** In each evaluation trial, no more than 1 out of 10 human-written submissions should receive the high-confidence AI label.

The human-written evaluation set will consist of at least 10 samples of my own writing, written before the evaluation trials begin. The exact same samples will be used in every trial without modification. Each sample must contain at least 100 words.

**Why this matters:** Using pre-existing, personally written samples creates a fixed baseline that cannot be adjusted to fit evaluation results. Reusing the same samples across trials makes the results comparable and helps measure whether the system incorrectly flags genuine human writing.

## 2. Score separation

**Target:** In each evaluation trial:

- The average combined score for AI-generated samples must be at least 0.15 higher than the average combined score for human-written samples.
- At least 70% of AI-generated samples must receive a combined score higher than the average combined score of the human-written samples.

**Why this matters:** The difference in average scores measures overall separation between the two groups. The second requirement ensures that the separation is not driven only by a small number of unusually high-scoring AI samples. Together, these measurements evaluate both the overall score difference and its consistency across individual AI samples.

## 3. Label coverage

**Target:** Each evaluation trial should produce all three possible labels at least once: `human`, `unsure`, and `ai`.

**Why this matters:** The system should not classify every submission as AI or human. The unsure category is important because the signals may disagree or produce a score that does not justify a confident decision.

## 4. Appeal workflow

**Target:** Every valid appeal submitted for an existing content ID should receive a successful response, create an audit-log entry with status `under_review`, and preserve the original decision in the audit history.

**Why this matters:** Writers should have a way to challenge a decision. An appeal should create a review record rather than silently changing the original score or automatically rerunning the detector.

## 5. Invalid submission handling

**Target:** Every submission with missing, empty, or non-string text, or a missing or invalid creator ID, should receive a 4xx response and should not receive a normal classification.

**Why this matters:** Invalid requests should be rejected clearly rather than causing unexpected errors or creating misleading classification records.
