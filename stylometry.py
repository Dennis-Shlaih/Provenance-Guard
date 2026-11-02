"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""


import re
import statistics
import unicodedata


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ────────────────────────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    Measures sentence-length variation using the coefficient of variation.

    Returns:
        A nonnegative float. Lower values mean more uniform sentence lengths.
        Fewer than two sentences return 0.0 because spread cannot be calculated.
    """
    sentence_list = sentences(text)

    # Standard deviation requires at least two observations.
    if len(sentence_list) < 2:
        return 0.0

    # Measure each sentence by its number of words.
    lengths = [len(words(sentence)) for sentence in sentence_list]

    mean_length = statistics.mean(lengths)

    # Avoid division by zero for sentences containing no recognized words.
    if mean_length == 0:
        return 0.0

    # Coefficient of variation = standard deviation / mean.
    return statistics.stdev(lengths) / mean_length


def type_token_ratio(text: str) -> float:
    """
    Measures vocabulary variety: unique words / total words.

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.
    """
    word_list = words(text)

    if not word_list:
        return 0.0

    unique_words = set(word_list)

    return len(unique_words) / len(word_list)


def punctuation_density(text: str) -> float:
    """
    Measures the proportion of characters classified as Unicode punctuation.

    Returns:
        A float between 0 and 1.
    """
    if not text:
        return 0.0

    punctuation_count = sum(
        1 for char in text
        if unicodedata.category(char).startswith("P")
    )

    return punctuation_count / len(text)


# ── Combining them ───────────────────────────────────────────────────────────


def style_signal(text: str) -> float:
    """
    Combines sentence-length variation and vocabulary variety
    into a 0–1 AI-likelihood score.

    Higher means more likely AI according to this heuristic.

    Sentence length spread:
        Lower variation = more AI-like.
        Transform using 1 / (1 + CV).

    Type-token ratio:
        Lower vocabulary variety = more AI-like.
        Transform using 1 - TTR.

    Both metrics receive equal weight.

    Punctuation density is measured separately but excluded from
    the score until a defensible scoring relationship is established.
    """
    sentence_list = sentences(text)
    spread = sentence_length_spread(text)
    ttr = type_token_ratio(text)

    # Insufficient sentences to measure variation reliably.
    if len(sentence_list) < 2:
        spread_score = 0.5
    else:
        spread_score = 1 / (1 + spread)

    # Insufficient words to measure vocabulary variety.
    if not words(text):
        ttr_score = 0.5
    else:
        ttr_score = 1 - ttr

    # Equal weighting of the two active metrics.
    score = (spread_score + ttr_score) / 2

    return round(max(0.0, min(1.0, score)), 4)



if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
