"""
Combines the Model, Burstiness, and Style signals into one score.
"""

import config


def combine_signals(model_score, burstiness_score, style_score=None):
    combined = (
        0.50 * model_score
        + 0.50 * burstiness_score
    )
    return round(combined, 4)


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
    """Return the score range associated with each label."""
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]