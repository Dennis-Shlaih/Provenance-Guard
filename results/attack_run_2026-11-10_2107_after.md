# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 21:07
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `dfc91575-73b6-4155-93bd-a8f1d68de181` | human | 0.507 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `f48c8200-2b09-4b38-900f-6e9694ae8477` | unsure | 0.071 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `9954a837-a61d-42d6-8a77-fde48b19bcdc` | unsure | 0.213 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `a03a3eb2-8ef6-4b25-a16c-8088bebfbc1a` | unsure | 0.162 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `282771e0-e314-4730-8e82-71001837b0fb` | human | 0.311 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `1c431684-f033-4052-ac3d-cbd35188b043` | unsure | 0.036 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `2900b126-460c-45be-ba79-c266b6cfadbe` | unsure | 0.061 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `b882926d-ce18-4379-ab72-a8945816601f` | human | 0.437 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `36c8ace9-2089-416e-ae23-99702f042687` | unsure | 0.265 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `afd47d1a-4da9-4907-8c64-9808879ad04e` | ai | 0.818 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `683eb225-2107-4008-ba69-edcccfc0a432` | unsure | 0.171 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `74ae3bdf-3b70-4de5-b45d-6d3a7d3f978c` | ai | 0.382 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `4f2e2689-ace0-4250-8dec-8bdb733a476c` | ai | 0.465 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `a54f0100-267e-4d0c-80d2-508f710e0c14` | ai | 0.480 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `58327eba-f146-4aaf-9862-c30dcc859f79` | ai | 0.500 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `157da1ff-6836-4a45-acb6-bcad6a39cabd` | ai | 0.553 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `681b125c-8ded-429c-9965-60be768a0a66` | ai | 0.603 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `c31d0d97-917a-4a63-b0d2-982e3aa15006` | human | 0.342 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `64edb068-7aa8-4ba1-9789-fe295561e073` | unsure | 0.139 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `54c6233a-d75c-4ebe-a4e9-fde6fb4c4eb1` | human | 0.531 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `0440fa14-4e37-49d3-90af-22b04ab580b4` | unsure | 0.100 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `77a8b13b-fb85-4131-ba11-1889616a2614` | unsure | 0.037 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `a301814a-5108-478c-9e21-5200fdee5d4b` | unsure | 0.138 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `52b7d2d9-7bcb-4c6b-8a78-bc6e05798392` | unsure | 0.083 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `2bbdfbfa-7506-493e-856d-b1d4f234ef79` | human | 0.875 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `1f878d87-9d74-47b3-903f-fdc8b4822e22` | human | 0.608 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `fe15b091-56ea-4f2b-97bd-57f5836ea3c1` | ai | 0.621 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `ed7393fb-ef4b-406a-a028-f6160bf502ba` | ai | 0.745 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `6901239a-1573-497e-8ff9-5d7a733ee6da` | ai | 0.610 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `263ca708-f520-4af6-b279-b9a0e1dac908` | ai | 0.905 | HELD |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `42716a68-d132-41a5-afcf-0f63a33d8c22` | human | 0.832 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `364e34a1-e4b3-46b2-b4fa-54d5d2669fe8` | human | 0.832 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `86060ca2-b8b2-4d77-bae8-6ea10d27e818` | human | 0.832 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4a02a0a9-a61f-4d06-8d8f-521b8bee6a05` | human | 0.832 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f169c770-903e-4033-adab-a0e35a30cf2d` | human | 0.832 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2c5bedd3-c8f4-4199-97c1-52b7e0bdd947` | human | 0.832 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `574f78ac-b75a-4a7d-8815-adbe3f5729f9` | human | 0.832 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cab1c63a-efdb-4363-ba0e-56754fbbd156` | human | 0.832 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6758ef32-954c-4804-9331-147fb1fe1014` | human | 0.832 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `10406810-bcca-431a-aeab-e7da65c87599` | human | 0.832 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "dfc91575-73b6-4155-93bd-a8f1d68de181",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.507,
  "model_score": 0.1635,
  "style_score": 0.4955,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "f48c8200-2b09-4b38-900f-6e9694ae8477",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.0706,
  "model_score": 0.5943,
  "style_score": 0.3583,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "9954a837-a61d-42d6-8a77-fde48b19bcdc",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.2126,
  "model_score": 0.6662,
  "style_score": 0.4266,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "a03a3eb2-8ef6-4b25-a16c-8088bebfbc1a",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.162,
  "model_score": 0.6114,
  "style_score": 0.4898,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "282771e0-e314-4730-8e82-71001837b0fb",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3111,
  "model_score": 0.3212,
  "style_score": 0.4143,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "1c431684-f033-4052-ac3d-cbd35188b043",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.0359,
  "model_score": 0.5727,
  "style_score": 0.3537,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "2900b126-460c-45be-ba79-c266b6cfadbe",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.061,
  "model_score": 0.5862,
  "style_score": 0.3634,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "b882926d-ce18-4379-ab72-a8945816601f",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.4373,
  "model_score": 0.2452,
  "style_score": 0.3898,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "36c8ace9-2089-416e-ae23-99702f042687",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.265,
  "model_score": 0.7042,
  "style_score": 0.4173,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "afd47d1a-4da9-4907-8c64-9808879ad04e",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.818,
  "model_score": 0.9792,
  "style_score": 0.6984,
  "label": "This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "683eb225-2107-4008-ba69-edcccfc0a432",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.1706,
  "model_score": 0.6175,
  "style_score": 0.4887,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "74ae3bdf-3b70-4de5-b45d-6d3a7d3f978c",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.382,
  "model_score": 0.7387,
  "style_score": 0.5478,
  "label": "This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "4f2e2689-ace0-4250-8dec-8bdb733a476c",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.4652,
  "model_score": 0.8051,
  "style_score": 0.515,
  "label": "This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "a54f0100-267e-4d0c-80d2-508f710e0c14",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.48,
  "model_score": 0.8329,
  "style_score": 0.4614,
  "label": "This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "58327eba-f146-4aaf-9862-c30dcc859f79",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.5001,
  "model_score": 0.8005,
  "style_score": 0.5987,
  "label": "This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "157da1ff-6836-4a45-acb6-bcad6a39cabd",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.553,
  "model_score": 0.8814,
  "style_score": 0.4619,
  "label": "This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "681b125c-8ded-429c-9965-60be768a0a66",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.6025,
  "model_score": 0.8816,
  "style_score": 0.5601,
  "label": "This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c31d0d97-917a-4a63-b0d2-982e3aa15006",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3421,
  "model_score": 0.3223,
  "style_score": 0.3489,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "64edb068-7aa8-4ba1-9789-fe295561e073",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.1392,
  "model_score": 0.4625,
  "style_score": 0.3341,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "54c6233a-d75c-4ebe-a4e9-fde6fb4c4eb1",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.531,
  "model_score": 0.2044,
  "style_score": 0.3249,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "0440fa14-4e37-49d3-90af-22b04ab580b4",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.1003,
  "model_score": 0.5943,
  "style_score": 0.4177,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "77a8b13b-fb85-4131-ba11-1889616a2614",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.037,
  "model_score": 0.4998,
  "style_score": 0.4266,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "a301814a-5108-478c-9e21-5200fdee5d4b",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.1384,
  "model_score": 0.6401,
  "style_score": 0.3565,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "52b7d2d9-7bcb-4c6b-8a78-bc6e05798392",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.0834,
  "model_score": 0.5583,
  "style_score": 0.4919,
  "label": "We couldn't confidently distinguish between human and AI-generated writing. Your writing may have been entirely human-written.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "2bbdfbfa-7506-493e-856d-b1d4f234ef79",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.875,
  "model_score": 0.0,
  "style_score": 0.25,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "1f878d87-9d74-47b3-903f-fdc8b4822e22",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.6082,
  "model_score": 0.0112,
  "style_score": 0.75,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "fe15b091-56ea-4f2b-97bd-57f5836ea3c1",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.6214,
  "model_score": 0.9976,
  "style_score": 0.25,
  "label": "This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "ed7393fb-ef4b-406a-a028-f6160bf502ba",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.7453,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "6901239a-1573-497e-8ff9-5d7a733ee6da",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.6096,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "263ca708-f520-4af6-b279-b9a0e1dac908",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.9049,
  "model_score": 0.9876,
  "style_score": 0.8469,
  "label": "This text has patterns that are strongly associated with AI-generated writing. This is not proof that AI was used.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "42716a68-d132-41a5-afcf-0f63a33d8c22",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.8319,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "364e34a1-e4b3-46b2-b4fa-54d5d2669fe8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.8319,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "86060ca2-b8b2-4d77-bae8-6ea10d27e818",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.8319,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "4a02a0a9-a61f-4d06-8d8f-521b8bee6a05",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.8319,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "f169c770-903e-4033-adab-a0e35a30cf2d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.8319,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "2c5bedd3-c8f4-4199-97c1-52b7e0bdd947",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.8319,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "574f78ac-b75a-4a7d-8815-adbe3f5729f9",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.8319,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "cab1c63a-efdb-4363-ba0e-56754fbbd156",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.8319,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "6758ef32-954c-4804-9331-147fb1fe1014",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.8319,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "10406810-bcca-431a-aeab-e7da65c87599",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.8319,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "This text has patterns that are more consistent with human writing. This is not proof of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
