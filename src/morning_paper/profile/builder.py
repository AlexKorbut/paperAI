from __future__ import annotations

import logging

from ..embeddings import Embedder
from ..llm.client import AnthropicClient
from ..models import InterestProfile, Signal
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
) -> InterestProfile:
    """Tag signals, aggregate weights, return updated InterestProfile.

    When an embedder is supplied, the profile's strongest topics and entities are
    embedded into ``interest_vectors`` so retrieval can match news semantically
    (and cross-lingually). Without one, vectors stay empty and ranking falls back
    to keyword overlap.
    """
    if not signals:
        return existing or InterestProfile(user_id=user_id, output_lang=output_lang)

    tagged = tag_signals(signals, client=client)
    topics, entities = aggregate_weights(
        tagged,
        existing_topics=existing.topics if existing else None,
        existing_entities=existing.entities if existing else None,
    )
    interest_vectors = _build_interest_vectors(topics, entities, embedder)
    return InterestProfile(
        user_id=user_id,
        output_lang=output_lang,
        topics=topics,
        entities=entities,
        interest_vectors=interest_vectors,
    )


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
