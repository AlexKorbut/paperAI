from __future__ import annotations

import logging

from .feeds import Candidate
from ..embeddings import Embedder, max_similarity
from ..models import InterestProfile

logger = logging.getLogger(__name__)


def rank_candidates(
    candidates: list[Candidate],
    profile: InterestProfile,
    *,
    top_n: int = 40,
    embedder: Embedder | None = None,
    semantic_weight: float = 0.6,
) -> list[Candidate]:
    """Score candidates against the profile and return the top_n.

    Two signals are blended:
      * keyword overlap with profile topics/entities (always available), and
      * semantic similarity of the candidate to the profile's interest vectors
        (only when an embedder is supplied and the profile carries vectors).

    Semantic matching is what makes cross-lingual retrieval work — a Spanish
    article and a Russian interest land in the same embedding space — so when
    it is available we lean on it (``semantic_weight``). Without an embedder we
    fall back to keyword-only scoring, preserving the original behaviour.
    """
    keyword = {c.id: _keyword_score(c, profile) for c in candidates}

    semantic = _semantic_scores(candidates, profile, embedder) if embedder else {}
    w = semantic_weight if semantic else 0.0

    for c in candidates:
        c.score = w * semantic.get(c.id, 0.0) + (1.0 - w) * keyword[c.id]

    return sorted(candidates, key=lambda x: x.score, reverse=True)[:top_n]


def _keyword_score(candidate: Candidate, profile: InterestProfile) -> float:
    text = (candidate.title + " " + candidate.body).lower()
    score = 0.0

    for topic, weight in profile.topics.items():
        if topic.lower() in text:
            score += weight

    for entity, weight in profile.entities.items():
        if entity.lower() in text:
            score += weight * 0.5

    max_possible = sum(profile.topics.values()) + sum(v * 0.5 for v in profile.entities.values())
    if max_possible > 0:
        score = score / max_possible

    return score


def _semantic_scores(
    candidates: list[Candidate],
    profile: InterestProfile,
    embedder: Embedder,
) -> dict[str, float]:
    """Cosine similarity of each candidate to the nearest interest vector, in [0, 1].

    Returns an empty dict (caller falls back to keyword-only) if the profile has
    no interest vectors or the embedding call fails.
    """
    if not profile.interest_vectors:
        return {}
    try:
        vectors = embedder.embed([f"{c.title} {c.body}".strip() for c in candidates])
    except Exception as exc:  # noqa: BLE001 - degrade to keyword-only on any failure
        logger.warning("semantic ranking unavailable (embedding failed): %s", exc)
        return {}
    if len(vectors) != len(candidates):
        logger.warning("embedder returned %d vectors for %d candidates; skipping semantic ranking",
                       len(vectors), len(candidates))
        return {}

    scores: dict[str, float] = {}
    for c, vec in zip(candidates, vectors):
        # Map cosine [-1, 1] -> [0, 1] so it blends with the normalised keyword score.
        scores[c.id] = (max_similarity(vec, profile.interest_vectors) + 1.0) / 2.0
    return scores
