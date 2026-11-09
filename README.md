# Provenance Guard

## What This Does
 
A submission moves through the following steps:
 
1. **Receive the submission:** The `/submit` endpoint accepts the writer's text and `creator_id`.
2. **Validate the input:** The service checks that the required fields are present and valid before processing the submission.
3. **Generate a content ID:** The service assigns the submission a unique `content_id` so its decision can be identified and appealed later.
4. **Calculate the model signal:** The detector analyzes the text's predictability using GPT-2 and returns a model score between 0 and 1.
5. **Calculate the style signal:** The stylometry module measures sentence-length variation and vocabulary variety and combines them into a style score between 0 and 1. Punctuation density is also calculated, but only as a diagnostic. It is not part of the score.
6. **Combine and classify:** `scoring.py::combine_signals` merges both signals into one score, and `scoring.py::score_to_label` assigns one of three labels: `human`, `unsure`, or `ai`.
7. **Record and return the decision:** The service records the content ID, creator ID, individual signal scores, combined score, label, and status in the audit log. The response returns the content ID, guess, confidence, label, model score, and style score.
---
 
## Signals and Scoring
 
### Signal one: the model signal
 
The model signal uses GPT-2 to calculate the perplexity of a submission. Perplexity measures how predictable a sequence of words is to a language model. Lower perplexity means the model finds the text more predictable. Higher perplexity means it finds the text less predictable.
 
The detector converts perplexity into a score between 0 and 1 using a logistic curve on perplexity. A higher score means the text is more predictable to GPT-2 and therefore receives a higher AI-likelihood score under this heuristic.
 
**Scoring parameters (in `detector.py`):**
 
```text
midpoint:   45.0   (perplexity that maps to a score of 0.5)
steepness:  1.6    (how sharply the score moves either side of the midpoint)
```
 
These are the values supplied with the starter code. I have not changed them. The Rich Dad/Poor Dad human summary scores 0.8181 on this signal, which suggests the midpoint may be low for plain writing. Moving it would be a scoring decision, and I am not making that decision from a handful of samples that I also used to look for problems. Any change needs a fresh set and a note here.
 
**What it can't see:** The model cannot determine who wrote a submission. Predictable human writing, such as conventional wording and simple sentences, can receive a high AI-likelihood score. Unusual or complex AI-generated writing can receive a lower score. The score is also affected by vocabulary, subject matter, and length. It is a measure of predictability, not proof of authorship and not a calibrated probability.
 
### Signal two: the style signal
 
The style signal measures writing characteristics without attempting to understand the meaning of the submission. It calculates three metrics:
 
- **Sentence-length spread:** variation in sentence lengths, measured as the coefficient of variation (CV) of sentence length in words. More uniform sentences receive a higher AI-likelihood score.
- **Type-token ratio (TTR):** unique words divided by total words. Lower vocabulary variety receives a higher AI-likelihood score.
- **Punctuation density:** the proportion of characters classified as punctuation by Unicode, including em dashes, en dashes, curly quotes and apostrophes, and ellipses.
**How the metrics are combined:** the style score uses sentence-length spread and TTR with equal weight.
 
- Sentence-length spread is transformed with `1 / (1 + CV)`. Lower variation gives a higher score.
- TTR is transformed with `1 - TTR`. Lower variety gives a higher score.
Punctuation density is calculated and reported as a diagnostic but is excluded from the style score. I could not defend a specific direction or strength of relationship between punctuation frequency and AI authorship.
 
**What it can't see:**
 
- It cannot establish authorship or understand why a writer made a choice. Humans can write evenly and repeat vocabulary, and AI can deliberately vary sentence length and vocabulary.
- Cheap changes that alter the shape of a text without changing what it says move this signal: typos, splitting or merging sentences, pasted quotations. The later attack set targets exactly this.
- TTR falls as text gets longer, so texts of different lengths are not directly comparable. I keep calibration samples in a narrow length band and record word counts rather than correcting for length.
- Very short texts do not give enough sentences for a meaningful CV.
- Plain, uniform human writing (reports, summaries, instructions) can look AI-like to this signal.
### The combining rule
 
**Where it lives:** `scoring.py::combine_signals` applies the weights from `config.py`. `scoring.py::score_to_label` applies the thresholds.
 
The two signals receive equal weight. I have too little evidence to justify favoring one.
 
```text
Combined Score = (0.50 × Model Score) + (0.50 × Style Score)
```
 
**Observation about the two signals:** the only matched human/AI pair in the current test results is the geology pair. On that pair the model signal separates the samples (AI 0.6828, human 0.4749), while the style signal ranks them the wrong way (human 0.5779, AI 0.5149). Across the four logged runs, style scores range only from 0.5149 to 0.5779, a narrow band, so with equal weights the style signal pulls the combined score toward the middle. One pair is not enough to say how the two signals behave in general. I am keeping equal weights as the baseline, recording this as an observation, and not re-weighting.
 
**Disagreement safeguard:** an earlier draft proposed returning `unsure` when the two signals differ by 0.30 or more. It was removed because it was tuned on a single sample that was later replaced. The underlying risk remains: the Rich Dad/Poor Dad human summary has a model score of 0.8181 against a style score of 0.5652, a gap of about 0.25. This is something to revisit with a larger set.
 
### Classification thresholds
 
Configured in `config.py` and applied by `scoring.py::score_to_label`:
 
| Combined score | `guess` |
|---|---|
| ≤ 0.35 | `human` |
| > 0.35 and < 0.69 | `unsure` |
| ≥ 0.69 | `ai` |
 
Thresholds are inclusive: exactly 0.35 is `human` and exactly 0.69 is `ai`.
 
**Threshold history (and why it does not hold up):** the AI threshold started at 0.65. I raised it to 0.69 because, in an earlier calibration run, the human-written Rich Dad/Poor Dad summary scored a combined 0.6849, while a paired AI sample scored 0.7002. That choice was fitted to a window between two samples. The earlier run is not reproduced in this README, and its figures came from text versions that were later replaced, so they should not be relied on. The version of the Rich Dad/Poor Dad summary I am keeping scores a combined 0.69165 and is classified `ai`, exceeding the threshold by about 0.0017. So the 0.69 threshold does not protect the sample it was chosen for.
 
I am not raising the threshold again to fix this. That would repeat the same mistake on the same evidence. The sample stays in this document as a documented false positive. The 0.69 value stays as a provisional setting, to be evaluated on the separate human-written evaluation set, which must not be used for tuning.
 
**Labels:** The service returns one of three reader-facing messages corresponding to the human, unsure, and ai classifications. The exact wording and score ranges are documented under Label Variants.
 
**Confidence field:** the API returns `confidence = abs(combined_score - 0.5) × 2`. This is distance from the midpoint, not a calibrated probability that the label is correct. Because the thresholds are asymmetric, a `human` at exactly 0.35 has confidence 0.30, which is lower than a borderline `ai` at 0.69 (0.38).
 
### Integration test results
 
These results come from submitting samples through the real `POST /submit` endpoint. This is an integration test, not an evaluation. These submissions were used to verify the integration pipeline and investigate scoring behavior. They are development samples, not an independent evaluation set.
 
| Sample | Model | Style | Combined | `guess` | Audit entry |
|---|---:|---:|---:|---|---|
| Human geology | 0.4749 | 0.5779 | 0.5264 | unsure | `209a1da8` |
| Original AI geology | 0.6828 | 0.5149 | 0.5989 | unsure | `72842af9` |
| Human Rich Dad/Poor Dad summary | 0.8181 | 0.5652 | 0.6917 | ai | `9f97ddde` |
| Lightly edited AI geology | 0.6762 | 0.5149 | 0.5956 | unsure | `a345f846` |
 
The lightly edited passage changes two phrases in the original AI geology sample. Its model score decreased from 0.6828 to 0.6762, while its style score remained 0.5149. The combined score decreased by 0.0033, and both versions received `unsure`. These two substitutions had little effect on the final classification, although this single comparison does not establish general resistance to editing.
 
**What the results show:**
 
- **Geology separation is small.** Original AI scored 0.5989 against 0.5264 for human, a gap of 0.0725. The model signal separates the pair by +0.2079, and the style signal gets it backwards by 0.0630. Both samples are `unsure`.
- **Rich Dad/Poor Dad is a false positive.** The human-written summary was classified `ai` at a combined 0.6917 (stored as 0.69165), driven by a model score of 0.8181. It clears the threshold by about 0.0017, so the result is fragile. But it is the failure the system is meant to avoid, and it is exactly the plain, school-style writing the model signal is most likely to accuse.
These results do not establish reliable human–AI separation. The model signal provides some separation on the geology pair, but the style signal works against it, and the human Rich Dad/Poor Dad sample crosses the AI threshold. The equal-weight combination does not eliminate these weaknesses. A larger, independent evaluation set is needed before drawing conclusions about detection performance or changing the scoring parameters.
 
### Audit logging
 
Each submission gets a unique `content_id`. Each log entry records:
 
- `content_id` and `creator_id`
- `model_score`, `style_score`, `combined_score`
- `guess`: the short classification (`human`, `unsure`, or `ai`)
- `label`: the finalized user-facing message corresponding to the classification.
- `timestamp` and `status`
Recording all three scores makes it possible to investigate disagreements between the signals.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35  | This text has patterns that are more consistent with human writing. This is not proof of who wrote it. |
| unsure | Above 0.35 and below 0.69 | We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written. |
| high-confidence AI | 0.69–1.00 | This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used. |

**Why I worded the "unsure" one this way:**

I chose this wording because an uncertain result should not make the writer feel accused of using AI. The system cannot reliably determine who wrote something, so the message explicitly acknowledges that the writing may have been entirely human-written. It also avoids presenting uncertainty as a negative judgment about the writer or their work.

---

## Sample Run

**A submission**

```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "text": "One feature in the stories and cult practices for Demeter that highlights the connection between Greek gods and the natural world is the timing and content of the Thesmophoria and Haloa rituals. These practices were scheduled around the agricultural calendar and used explicitly sexual symbols. The women were ritually working alongside the earth’s agricultural cycle, using their bodies and words as instruments to influence whether the seeds took hold. This detail justifies existing social arrangements by naturalizing and reinforcing a gendered division of labor by grounding it in the actions of a goddess.",
    "creator_id": "milestone-5-human-label"
  }'

```

**Response:**

```json
{
  "combined_score": 0.32715,
  "confidence": 0.3457,
  "content_id": "819d9a8a-da66-44c3-ad6a-fbfe94ef4268",
  "guess": "human",
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "model_score": 0.1572,
  "style_score": 0.4971
}

```

### Appeal Example

A writer can appeal an existing classification by submitting the original `content_id` and an explanation.

**Request:**

```bash
curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "9f97ddde-a1a5-4bac-b4f7-7849ecf9b14f",
    "reasoning": "I wrote this submission myself. The classification does not reflect how I created the text, and I would like it reviewed."
  }'
```

**Response:**

```json
{
  "content_id": "9f97ddde-a1a5-4bac-b4f7-7849ecf9b14f",
  "message": "Your appeal has been recorded and the submission is under review.",
  "status": "under_review"
}

```

**Audit log entries:**

Original decision:

```json
{
  "content_id": "9f97ddde-a1a5-4bac-b4f7-7849ecf9b14f",
  "creator_id": "milestone-4-test",
  "guess": "ai",
  "model_score": 0.8181,
  "style_score": 0.5652,
  "combined_score": 0.6916500000000001,
  "status": "decided"
}

```

Appended appeal event:

```json
{
  "content_id": "9f97ddde-a1a5-4bac-b4f7-7849ecf9b14f",
  "creator_id": "milestone-4-test",
  "event": "appeal",
  "reasoning": "I wrote this submission myself. The classification does not reflect how I created the text, and I would like it reviewed.",
  "status": "under_review"
}

```

The appeal creates a separate audit event rather than overwriting the original decision. This preserves the original classification and records that the writer requested a review.

---

## How I Used AI

**Moment 1: Reviewing my acceptance criteria (Claude)**
 
- *What I asked for:* I wrote all five acceptance criteria myself, then pasted them into Claude and asked what it thought of them. I asked for a review of whether each one could be checked by someone who couldn't ask me what I meant. I did not ask it to write any criteria.
- *What came back:* A criterion-by-criterion review. It said criterion 1 didn't say who wrote the ten human samples or what counted as the high-confidence AI label, and that one false positive in ten is a loose bar. It also said criterion 2 compares averages, which can hide overlapping scores, and that "combined score" and the 0.15 target needed to be defined and justified.
- *What I changed:* I revised the criteria using that review and my own follow-up decisions. The human samples must be my own writing, fixed before each trial, and above a minimum length. I described 0.15 as a starting target that measures average separation, not whether each sample is classified correctly. I stated that label coverage shows the labels are reachable, not that they are accurate. I decided to verify appeals manually because the evaluation runner doesn't test them. I extended criterion 5 to cover malformed JSON and JSON that isn't an object, as well as the individual fields.

**Moment 2: Generating the AI-written samples (ChatGPT)**
 
- *What I asked for:* I used ChatGPT to generate the AI-written calibration samples. For each of my human-written samples I asked for an AI-written passage on the same topic (geology, the Rich Dad, Poor Dad summary, and others). Matching the topics keeps subject and vocabulary controlled, so each pair mostly compares writing style.
- *What came back:* Essay-style paragraphs of roughly 100 to 160 words, close to the length of the matching human samples.
- *What I changed:* I used the AI samples as generated, with one exception. For the lightly edited sample, I changed two phrases in the AI geology passage by hand. I treat that sample as a derivative of the original, not an independent one. All of my human samples are my own writing, and none of them were generated. All of the AI samples come from a single generator, so my results say nothing about how the detector handles text from other models.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**

These limits balance normal usage with protection against automated abuse. A legitimate writer might submit several pieces of work within an hour, so 10 submissions per minute provides room for occasional bursts without unnecessarily blocking them. The daily limit of 200 allows repeated use throughout the day while restricting sustained automated requests. A script attempting to send thousands of variations to map the detection thresholds would quickly encounter the limits.

**What a caller counts as:** 

Requests are grouped by their creator_id, so submissions from the same creator share a rate-limit bucket. This makes the limits consistent across requests from the same identified writer. However, a script could potentially bypass this approach by generating different creator IDs, which is a limitation of per-creator rate limiting.

Command: python run_attacks.py --flood 15

200 200 200 200 200 200 200 200 200 200 429 429 429 429 429

```Results: 10 successful submissions and 5 rate-limited submissions.```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `882c7d8b-c2b9-4522-b569-2e1fef1782a7` | human | 0.341 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `cb5dd3ea-7703-4453-80b2-77e533e75a44` | unsure | 0.047 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `3d0a47c2-d88a-4bf3-88b3-cfe14d3973d6` | unsure | 0.093 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `7d261b98-220b-4250-87b3-578946eabd8c` | unsure | 0.101 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `264b6082-c554-4cbd-a546-d3c0e36572f6` | unsure | 0.265 | HELD |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `6ccacc50-d093-45da-be33-625584728e4b` | unsure | 0.074 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `dbfe1ad8-00c9-4c74-9faa-c4146fad5935` | unsure | 0.050 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `87892bdc-6d5e-4b4e-bf70-5c3dc36adcf1` | human | 0.365 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `ced8be72-86be-43e3-8f5f-7a140d315505` | unsure | 0.121 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `f4496a8e-748f-4a77-8dc1-da933f205476` | ai | 0.678 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `047e2a80-4b95-4064-bf6c-f46936ab79a7` | unsure | 0.106 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `b815cd1f-cae3-4941-a59f-4d84bab7ffb4` | unsure | 0.286 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `5b7e697c-73ba-4da2-b50e-16e69d0b48a8` | unsure | 0.320 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `3e0a36ac-61ab-4211-8251-428f90bb8529` | unsure | 0.294 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `bd3e1c40-678b-4139-88dc-88da259ce0c9` | ai | 0.399 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `4fffefb1-067b-4486-b4bf-70b992c24c49` | unsure | 0.343 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `48dc62a4-3f40-48be-91d1-ffa79bd36071` | ai | 0.442 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `e15d83cc-6a9f-48e0-9e34-09a78cf1bb25` | human | 0.329 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `44ed0a52-47f5-4889-b0f8-eb3f7a6063b5` | unsure | 0.203 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `5f573945-4465-43ba-9ac1-ff4cef1de3b3` | human | 0.471 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `74fbc1e5-8a4c-44f0-9cae-6fb96f7d2af1` | unsure | 0.012 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `dcf6b1cb-9af1-41cb-8574-e8aa8de9800c` | unsure | 0.074 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `7a22f17e-61c4-4bdb-a4dc-8a51efe23175` | unsure | 0.003 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `d19a96e6-c60a-40ba-85bd-3b7a860dc278` | unsure | 0.050 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `e2608f53-9432-4619-b095-034704330dcb` | human | 0.750 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `c22daaf0-51ef-4adf-91c1-9df2a61abe10` | unsure | 0.239 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `b69395b6-e0e5-4dac-9adb-bcfd1c642edb` | unsure | 0.248 | HELD |
| MF06 | malformed | text is emoji only | 200 | `ee744aa5-6099-460a-a0ce-3d236eee0cde` | ai | 0.497 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `daf70918-be5b-4f11-8aa7-dd3cc036a8a5` | ai | 0.406 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `f56be2cc-a151-4bf4-ad0a-33a14f8cf333` | ai | 0.835 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7de647c5-778d-43af-b6ee-3d4b1876c9ea` | human | 0.721 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `574f053d-27e2-42ac-b6a4-afd77cbb6114` | human | 0.721 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `12e6ebdc-e3da-4ecc-8e37-a7557d43b915` | human | 0.721 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7b251100-db85-420a-af5a-22893ac05f21` | human | 0.721 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ca790230-a695-4fd5-b891-921ecdf1336a` | human | 0.721 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3f4bce5e-04b0-4601-a46e-359dfb5b14cb` | human | 0.721 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f7993809-0614-4ac8-9d7c-7b65fa7f97ca` | human | 0.721 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `40803705-1597-4481-9039-b8d92376aa66` | human | 0.721 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cf672303-b11a-42a6-b5c3-497d2ca10fa8` | human | 0.721 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3aca3ef2-74eb-4d53-9d4d-d475a2927001` | human | 0.721 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

**Ten audit log entries from the run**

```json

{"timestamp":"2026-11-05T00:28:15+00:00","content_id":"882c7d8b-c2b9-4522-b569-2e1fef1782a7","creator_id":"attacker_EV01","guess":"human","model_score":0.1635,"style_score":0.4955,"combined_score":0.3295,"label":"This text has patterns that are more consistent with human writing. This is not proof of who wrote it.","status":"decided"}
{"timestamp":"2026-11-05T00:28:16+00:00","content_id":"87892bdc-6d5e-4b4e-bf70-5c3dc36adcf1","creator_id":"attacker_EV08","guess":"human","model_score":0.2452,"style_score":0.3898,"combined_score":0.3175,"label":"This text has patterns that are more consistent with human writing. This is not proof of who wrote it.","status":"decided"}
{"timestamp":"2026-11-05T00:28:18+00:00","content_id":"bd3e1c40-678b-4139-88dc-88da259ce0c9","creator_id":"attacker_FP05","guess":"ai","model_score":0.8005,"style_score":0.5987,"combined_score":0.6996,"label":"This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.","status":"decided"}
{"timestamp":"2026-11-05T00:28:18+00:00","content_id":"48dc62a4-3f40-48be-91d1-ffa79bd36071","creator_id":"attacker_FP07","guess":"ai","model_score":0.8816,"style_score":0.5601,"combined_score":0.72085,"label":"This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.","status":"decided"}
{"timestamp":"2026-11-05T00:28:19+00:00","content_id":"5f573945-4465-43ba-9ac1-ff4cef1de3b3","creator_id":"attacker_PI02","guess":"human","model_score":0.2044,"style_score":0.3249,"combined_score":0.26465,"label":"This text has patterns that are more consistent with human writing. This is not proof of who wrote it.","status":"decided"}
{"timestamp":"2026-11-05T00:28:19+00:00","content_id":"7a22f17e-61c4-4bdb-a4dc-8a51efe23175","creator_id":"attacker_PI05","guess":"unsure","model_score":0.6401,"style_score":0.3565,"combined_score":0.49829999999999997,"label":"We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.","status":"decided"}
{"timestamp":"2026-11-05T00:28:19+00:00","creator_id":"attacker_MF01","event":"rejected","status":"rejected","reason":"missing_or_invalid_text"}
{"timestamp":"2026-11-05T00:28:19+00:00","content_id":"e2608f53-9432-4619-b095-034704330dcb","creator_id":"attacker_MF03","guess":"human","model_score":0.0,"style_score":0.25,"combined_score":0.125,"label":"This text has patterns that are more consistent with human writing. This is not proof of who wrote it.","status":"decided"}
{"timestamp":"2026-11-05T00:28:21+00:00","content_id":"7de647c5-778d-43af-b6ee-3d4b1876c9ea","creator_id":"attacker_flood","guess":"human","model_score":0.0287,"style_score":0.25,"combined_score":0.13935,"label":"This text has patterns that are more consistent with human writing. This is not proof of who wrote it.","status":"decided"}
{"timestamp":"2026-11-05T00:28:22+00:00","creator_id":"attacker_flood","event":"rejected","status":"rejected","reason":"rate_limited","limit":"10 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP05 was a false positive: human-written technical documentation was classified as AI-generated. This is especially concerning because a writer could produce legitimate technical work and still be incorrectly flagged. The combined score was 0.6996, just above the AI threshold of 0.69. FP07 was another false positive involving human writing with deliberate repetition.

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

       [X] criteria.md has five numbered criteria, each naming a target
       [X] Each has a reason underneath
       [X] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [X] Two signals that measure DIFFERENT things, each with a named blind spot
       [X] Three label variants, all reachable, written out in full
       [X] POST /appeal changes status and writes to the log
       [X] Signals and Scoring names scoring.py::combine_signals
       [X] Sample Run: a submission AND an appeal, as pasted text
       [X] At least four new commits
       [X] Repository URL submitted — WRITE IT DOWN

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
