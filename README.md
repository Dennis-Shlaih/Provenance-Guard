# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

A submission moves through the following steps:

1. **Receive the submission:** The `/submit` endpoint accepts the writer's text and `creator_id`.
2. **Validate the input:** The service checks that the required fields are present and valid before processing the submission.
3. **Generate a content ID:** The service assigns the submission a unique `content_id` so its decision can be identified and appealed later.
4. **Calculate the model signal:** The detector analyzes the text's predictability using GPT-2 and returns a model score between 0 and 1.
5. **Calculate the style signal:** The stylometry module measures sentence length variation, vocabulary variety, and punctuation density, then produces a style score between 0 and 1.
6. **Combine and classify:** The scoring module combines both signals into one score and assigns one of three labels: `human`, `unsure`, or `ai`.
7. **Record and return the decision:** The service records the content ID, creator ID, individual signal scores, combined score, label, and status in the audit log. The response returns the content ID, guess, confidence, label, model score, and style score.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:**

The model signal uses GPT-2 to calculate the perplexity of a submission. Perplexity measures how predictable a sequence of words is to a language model. Lower perplexity means the model finds the text more predictable, while higher perplexity means it finds the text less predictable.

The detector converts perplexity into a score between 0 and 1, where a higher score represents greater AI-likelihood according to this heuristic.

**Why that might differ between human and AI writing:**

AI-generated writing can sometimes have predictable word choices and sentence structures. This signal attempts to capture those patterns by measuring how predictable the submitted text is to a language model.

**What it can't see:**

The model cannot determine who actually wrote the submission. Predictable human writing, such as conventional wording or simple sentences, can receive a high AI-likelihood score. Unusual or complex AI-generated writing can receive a lower score because it is less predictable. The score is also affected by vocabulary, subject matter, and writing style.

Perplexity is a measure of predictability, not proof of AI authorship or a calibrated probability that AI generated the text.

### Signal two — the style signal

**What it measures:**

The style signal measures writing characteristics without attempting to understand the meaning of the submission. It calculates three metrics:

- **Sentence length spread:** Measures variation in sentence lengths using the coefficient of variation (standard deviation divided by mean sentence length). Lower variation may indicate more uniform writing.
- **Type-token ratio:** Measures vocabulary variety by dividing the number of unique words by the total number of words. A lower ratio indicates more repeated vocabulary.
- **Punctuation density:** Measures the proportion of characters classified as punctuation by Unicode. This includes ASCII punctuation and typographic characters such as em dashes, en dashes, curly quotation marks, curly apostrophes, and ellipses.

**How the metrics are combined:**

The final style score uses sentence length spread and type-token ratio, giving each transformed metric equal weight:

- Sentence length spread is transformed using `1 / (1 + CV)`. Lower variation produces a higher AI-likelihood score.
- Type-token ratio is transformed using `1 - TTR`. Lower vocabulary variety produces a higher AI-likelihood score.

Punctuation density is still calculated and reported as a diagnostic metric, but it is excluded from the numerical style score. I chose not to include it because punctuation frequency alone does not provide a sufficiently defensible relationship with AI authorship.

The resulting style score ranges from 0 to 1, where a higher score represents greater AI-likelihood according to the implemented heuristic.

**Why that might differ between human and AI writing:**

AI-generated writing may sometimes exhibit more consistent sentence lengths and repeated vocabulary patterns. Human writing may show more variation in sentence structure and vocabulary. These metrics attempt to capture some of those differences.

**What it can't see:**

These measurements cannot establish authorship or understand why a writer chose particular words or sentence structures.

Humans can write consistently and repeat vocabulary, while AI can deliberately vary sentence lengths and vocabulary. Type-token ratio is also sensitive to text length, generally decreasing as a text becomes longer. Punctuation habits vary by individual, genre, and editing tools; frequent use of a particular punctuation mark, including em dashes, is not proof of AI authorship.

The metrics can also be affected by short submissions, which may not provide enough text to measure writing patterns reliably.

### The combining rule

**The design choice:**

The model signal and style signal receive equal weight in the combined score. However, neither signal should automatically override the other.

Calibration revealed that the model signal can assign a very high AI-likelihood score to conventional human writing. For example, one human-written sample received a model score of 0.9612 but a style score of 0.4668.

To account for this, the proposed combining rule includes a disagreement safeguard. If the absolute difference between the two signal scores is greater than or equal to 0.30, the system should return `unsure` rather than allow the weighted average to produce a potentially misleading confident classification.

When the signals do not exceed the disagreement cutoff, their scores are averaged using equal weights.

The combined score is a heuristic AI-likelihood score, not a calibrated probability of authorship.

**The numbers:**

Initial configuration:

```text
Model signal weight:       0.50
Style signal weight:       0.50
Disagreement cutoff:       0.30
Human threshold:           0.35
AI threshold:              0.65
```

Combining formula:

```text
Combined Score = (0.50 × Model Score) + (0.50 × Style Score)

Disagreement = abs(Model Score - Style Score)

If Disagreement >= 0.30:
    Label = unsure
Otherwise:
    Score <= 0.35: human
    Score >= 0.65: ai
    Otherwise: unsure
```

The combined score is interpreted using these thresholds:

- **Human:** Combined score is less than or equal to 0.35.
- **Unsure:** Combined score is greater than 0.35 and less than 0.65, or the disagreement safeguard is triggered.
- **AI:** Combined score is greater than or equal to 0.65, provided the disagreement safeguard is not triggered.

**Where it lives:** `scoring.py::combine_signals`

The model/style weights and classification thresholds are configurable in `config.py`. The 0.30 disagreement cutoff is part of the proposed rule above.

### Calibration results

I tested both signals on four deliberately chosen writing samples. The table records the model score, style score, and calculated combined score for each sample.

| Calibration input | Model score | Style score | Combined score |
|---|---:|---:|---:|
| Clearly AI | 0.7061 | 0.5848 | 0.6455 |
| Clearly human | 0.9612 | 0.4668 | 0.7140 |
| Formal human | 0.7155 | 0.5289 | 0.6222 |
| Lightly edited AI | 0.5084 | 0.5507 | 0.5296 |

The combined scores in this table are the equal-weight averages before applying the disagreement safeguard.

**What the results showed:**

- The clearly AI sample received relatively high scores from both signals.
- The clearly human sample received an extremely high model score despite a much lower style score. This demonstrates the model signal's vulnerability to predictable human writing.
- The formal human sample also received a higher model score than style score.
- The lightly edited AI sample received relatively neutral scores from both signals, showing that neither heuristic reliably identifies every AI-generated example.

The conventional human sample produced a signal difference of 0.4944, exceeding the initial disagreement cutoff. Under the proposed combining rule, it would receive `unsure` rather than `ai`.

These four examples are calibration observations, not proof that the detector reliably distinguishes human and AI writing. The disagreement cutoff and thresholds will need to be evaluated against a larger test set.

### Logging the three scores

Each successfully classified submission's audit-log entry is intended to record all three scores:

- `model_score`: Output from the GPT-2 perplexity-based signal.
- `style_score`: Output from the stylometric signal.
- `combined_score`: Result of the combining rule before classification.

Recording all three values makes it possible to investigate disagreements, understand unexpected classifications, and evaluate the individual signals separately.

The audit log also preserves the resulting label and decision status so that later evaluations and appeals can be traced to the original decision.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
