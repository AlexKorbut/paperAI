"""Embedding abstraction used by profile building and semantic ranking.

The concrete backend is Voyage AI (multilingual), but everything downstream
depends only on the small ``Embedder`` protocol, so tests can inject a fake and
the pipeline degrades gracefully (keyword-only ranking) when no API key is set.
"""

from __future__ import annotations

import logging
import math
from typing import Protocol, runtime_checkable

from .voyage import DEFAULT_MODEL, VoyageClient

logger = logging.getLogger(__name__)


@runtime_checkable
class Embedder(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text (same order)."""
        ...


class VoyageEmbedder:
    """Thin adapter binding a VoyageClient + model behind the Embedder protocol."""

    def __init__(self, client: VoyageClient | None = None, *, model: str = DEFAULT_MODEL) -> None:
        self._client = client or VoyageClient()
        self._model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        return self._client.embed(texts, model=self._model)


def get_embedder() -> Embedder | None:
    """Build the configured embedder, or ``None`` when no key/provider is set.

    Returning ``None`` is the signal for callers to fall back to keyword-only
    behaviour rather than failing the nightly run.
    """
    from ..config import get_settings

    settings = get_settings()
    key = settings.secrets.voyage_api_key
    if not key:
        return None
    if settings.file.embeddings.provider != "voyage":
        logger.warning(
            "unsupported embeddings provider %r; semantic ranking disabled",
            settings.file.embeddings.provider,
        )
        return None
    model = settings.file.embeddings.model or DEFAULT_MODEL
    return VoyageEmbedder(VoyageClient(key), model=model)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity in [-1, 1]; 0.0 for empty/zero vectors."""
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def max_similarity(vector: list[float], references: list[list[float]]) -> float:
    """Best cosine similarity of ``vector`` against any reference vector."""
    if not vector or not references:
        return 0.0
    return max(cosine_similarity(vector, ref) for ref in references)
