from __future__ import annotations

import logging

from ..embeddings import Embedder
from ..llm.client import AnthropicClient
from ..models import Feedback, InterestProfile, Signal
from .aggregator import aggregate_weights
from .tagger import tag_signals

logger = logging.getLogger(__name__)


def build_profile(
    user_id: str,
    signals: list[Signal],
    *,
    existing: InterestProfile | None = None,
    output_lang: str = "ru",
    client: AnthropicClient | None = None,
    embedder: Embedder | None = None,
    feedback: list[Feedback] | None = None,
) -> InterestProfile:
    """Tag signals, aggregate weights, fold in feedback, return InterestProfile.

    When an embedder is supplied, the profile's strongest topics and entities are
    embedded into ``interest_vectors`` so retrieval can match news semantically
    (and cross-lingually). Without one, vectors stay empty and ranking falls back
    to keyword overlap. In-product 👍/👎 ``feedback`` nudges topic/entity weights
    after aggregation so the profile tracks the user's evolving taste.
    """
    if not signals:
        base = existing or InterestProfile(user_id=user_id, output_lang=output_lang)
        return _apply_feedback(base, feedback)

    tagged = tag_signals(signals, client=client)
    topics, entities = aggregate_weights(
        tagged,
        existing_topics=existing.topics if existing else None,
        existing_entities=existing.entities if existing else None,
    )
    interest_vectors = _build_interest_vectors(topics, entities, embedder)
    profile = InterestProfile(
        user_id=user_id,
        output_lang=output_lang,
        topics=topics,
        entities=entities,
        interest_vectors=interest_vectors,
    )
    return _apply_feedback(profile, feedback)


def _apply_feedback(
    profile: InterestProfile, feedback: list[Feedback] | None
) -> InterestProfile:
    if not feedback:
        return profile
    from ..feedback import apply_to_profile

    try:
        return apply_to_profile(profile, feedback)
    except Exception as exc:  # noqa: BLE001 - feedback must never break profile build
        logger.warning("applying feedback failed: %s", exc)
        return profile


def _build_interest_vectors(
    topics: dict[str, float],
    entities: dict[str, float],
    embedder: Embedder | None,
    *,
    max_phrases: int = 12,
) -> list[list[float]]:
    """Embed the top interest phrases into vectors; ``[]`` if no embedder."""
    if embedder is None:
        return []

    # Highest-weight topics (as readable phrases) + entities, capped.
    phrases = [t.replace("/", " ").strip() for t, _ in
               sorted(topics.items(), key=lambda kv: kv[1], reverse=True)]
    phrases += [e for e, _ in sorted(entities.items(), key=lambda kv: kv[1], reverse=True)]
    phrases = [p for p in phrases if p][:max_phrases]
    if not phrases:
        return []
    try:
        return embedder.embed(phrases)
    except Exception as exc:  # noqa: BLE001 - profile build must not fail on embeddings
        logger.warning("interest-vector embedding failed: %s", exc)
        return []
