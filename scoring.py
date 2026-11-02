"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

Two functions live here, and both are stubs.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine the model and style signals using equal weighting.

    Each signal contributes 50% to the combined score.

    When the signals disagree, the average moves toward the middle,
    reflecting uncertainty rather than relying entirely on one signal.
    """
    return (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    )


def score_to_label(score: float) -> tuple[str, str]:
    """
    Convert the combined score into a machine-readable guess
    and an explanation intended for the person submitting the text.
    """

    if score >= config.AI_THRESHOLD:
        return (
            "ai",
            "This text has patterns that are strongly associated with "
            "AI-generated writing. This is not proof that AI was used."
        )

    if score <= config.HUMAN_THRESHOLD:
        return (
            "human",
            "This text has patterns that are more consistent with human "
            "writing. This is not proof of who wrote it."
        )

    return (
        "unsure",
        "We couldn't confidently distinguish between human and "
        "AI-generated writing. Your writing may have been entirely "
        "human-written."
    )


def label_ranges() -> list[tuple[str, str]]:
    """
    Return the score range associated with each label.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]