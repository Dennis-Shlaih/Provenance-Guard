"""
Signal one: the model signal.

This is the signal that "reads the text for meaning". It runs a language model
on your own machine and asks one question: **how predictable is this text?**

The idea is the one every AI-detection product is built on. A language model
writes by repeatedly picking a likely next word, so text a model produced tends
to be text a model finds easy to predict. Human writing wanders more — odd word
choices, abrupt turns, the specific rather than the typical.

The measure is called **perplexity**. Low perplexity means "I could have
guessed this"; high perplexity means "that surprised me". This module turns
that into a 0–1 score where **higher means more likely AI**.

    from detector import model_signal
    score = model_signal("some text")     # 0.0 human-ish … 1.0 AI-ish

Everything runs locally. No account, no key, no card.

⚠️ **The blind spot, which you have to name in Milestone 1.**

Predictability is not the same thing as authorship. What this signal actually
rewards is **common words in short, ordinary sentences** — and plenty of real
people write that way.

Someone writing in a second language, sticking to vocabulary they're sure of.
A younger writer. Anyone writing plainly on purpose. Measured against gpt2,
writing like that scores about as machine-like as machine writing does.

The reverse trips people up too: dense, ornate prose full of rare words often
scores as *human* on this signal, because rare words are exactly what a
language model fails to predict. Formality on its own doesn't decide it.

So the writers this signal is most likely to accuse are the ones with the
least room to argue back. That is structural rather than a bug you can fix,
and it is the person Milestone 1 asks you to follow through your service.

Don't take that on trust — it's a claim you can check. Milestone 4 has you run
four calibration inputs. Add a plainly-written human paragraph to them and see
for yourself where it lands.
"""

import math

import config

_model = None
_tokenizer = None


class DetectorUnavailable(RuntimeError):
    """The model couldn't be loaded — no download yet, or no disk."""


class TextTooShortError(ValueError):
    """The text is too short to produce a reliable perplexity score."""


def _load():
    """Load the model once and keep it. First call downloads ~550 MB."""
    global _model, _tokenizer
    if _model is not None:
        return _model, _tokenizer

    try:
        import torch  # noqa: F401
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise DetectorUnavailable(
            f"transformers or torch isn't installed ({exc}).\n"
            f"Run: pip install -r requirements.txt"
        ) from exc

    try:
        _tokenizer = AutoTokenizer.from_pretrained(config.DETECTOR_MODEL)
        _model = AutoModelForCausalLM.from_pretrained(config.DETECTOR_MODEL)
        _model.eval()
        print("Detector device:", next(_model.parameters()).device)
        print("Detector dtype:", next(_model.parameters()).dtype)   
    except Exception as exc:  # noqa: BLE001
        raise DetectorUnavailable(
            f"Couldn't load '{config.DETECTOR_MODEL}': {exc}\n"
            f"The first run downloads about 550 MB — check your connection and "
            f"that you have disk space free."
        ) from exc

    return _model, _tokenizer


def model_metrics(text: str) -> tuple[float, float]:
    """
    Run GPT-2 once and calculate:
      1. Perplexity from mean token prediction loss.
      2. Burstiness from variance in token prediction loss.

    Returns:
        (perplexity, loss_variance)
    """
    import torch
    import torch.nn.functional as F

    model, tokenizer = _load()

    encoded = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=config.DETECTOR_MAX_TOKENS,
    )

    input_ids = encoded["input_ids"]

    if input_ids.shape[1] < 3:
        raise TextTooShortError(
            "Text is too short to score — provide at least three tokens."
        )

    with torch.no_grad():
        output = model(input_ids)

    # GPT-2 predicts the next token.
    # The first token has no preceding context, so exclude it.
    logits = output.logits[:, :-1, :]
    targets = input_ids[:, 1:]

    # Calculate the individual negative log-likelihood
    # for every predicted token.
    token_losses = F.cross_entropy(
        logits.reshape(-1, logits.shape[-1]),
        targets.reshape(-1),
        reduction="none",
    )

    mean_loss = token_losses.mean()
    loss_variance = token_losses.var(unbiased=False)

    perplexity_value = torch.exp(mean_loss).item()
    variance_value = loss_variance.item()

    return float(perplexity_value), float(variance_value)

def model_score_from_perplexity(ppl: float) -> float:
    """Convert perplexity into the existing 0–1 Model Signal."""
    midpoint = 45.0
    steepness = 1.6

    score = 1.0 / (1.0 + (ppl / midpoint) ** steepness)
    return round(min(max(score, 0.0), 1.0), 4)


def burstiness_score_from_variance(variance: float) -> float:
    """Convert token-loss variance into the heuristic Burstiness Signal."""
    score = 1.0 / (1.0 + variance)
    return round(min(max(score, 0.0), 1.0), 4)


def model_signals(text: str) -> tuple[float, float]:
    """
    Calculate Model Signal and Burstiness Signal with one GPT-2 inference.

    Returns:
        (model_score, burstiness_score)
    """
    ppl, variance = model_metrics(text)

    model_score = model_score_from_perplexity(ppl)
    burstiness_score = burstiness_score_from_variance(variance)

    return model_score, burstiness_score


def perplexity(text: str) -> float:
    """Return the existing perplexity measurement."""
    ppl, _ = model_metrics(text)
    return ppl


def burstiness_signal(text: str) -> float:
    """Return the Burstiness Signal for a text."""
    _, variance = model_metrics(text)
    return burstiness_score_from_variance(variance)


def model_signal(text: str) -> float:
    """Return the existing Model Signal for a text."""
    ppl, _ = model_metrics(text)
    return model_score_from_perplexity(ppl)


def warm_up() -> str:
    """Load the model without scoring anything. Run this before class."""
    _load()
    return f"{config.DETECTOR_MODEL} loaded and ready."


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = (
            "The implementation of the proposed framework requires careful "
            "consideration of several key factors. First, it is important to "
            "note that the system must be able to handle a wide variety of "
            "different inputs. Additionally, the overall performance of the "
            "solution depends on a number of important variables."
        )
        print("(no text given — scoring a sample)\n")

    print(f"Loading {config.DETECTOR_MODEL} (first run downloads ~550 MB)…")
    for i in range(5):
        ppl = perplexity(text)
        score = 1.0 / (1.0 + (ppl / 45.0) ** 1.6)
        print(
            f"Run {i + 1}: "
            f"perplexity={ppl:.8f}, "
            f"model_signal={score:.8f}"
            )
