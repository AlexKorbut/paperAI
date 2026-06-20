"""NewsAPI.org retriever — optional, key-gated supplement to GDELT/RSS.

NewsAPI gives clean title + description + source metadata. Unlike GDELT it has
no per-article language field (language is a query parameter), so callers may
pass ``language`` to both filter and label results. Best-effort: any failure
returns an empty list and is logged, never raised.
"""

from __future__ import annotations

import hashlib
import logging

import httpx

from .feeds import Candidate

logger = logging.getLogger(__name__)

NEWSAPI_URL = "https://newsapi.org/v2/everything"


def build_newsapi_query(terms: list[str]) -> str:
    """OR-join terms; quote multi-word phrases (NewsAPI supports both)."""
    parts = [f'"{t}"' if " " in t else t for t in terms if t.strip()]
    return " OR ".join(parts)


def fetch_newsapi_candidates(
    terms: list[str],
    *,
    api_key: str,
    page_size: int = 50,
    language: str | None = None,
    timeout: float = 30.0,
) -> list[Candidate]:
    """Query NewsAPI /v2/everything for recent articles matching the terms."""
    query = build_newsapi_query(terms)
    if not query or not api_key:
        return []

    params = {
        "q": query,
        "pageSize": str(max(1, min(page_size, 100))),
        "sortBy": "publishedAt",
    }
    if language:
        params["language"] = language
    try:
        resp = httpx.get(
            NEWSAPI_URL,
            params=params,
            headers={"X-Api-Key": api_key},
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:  # noqa: BLE001 - retrieval is best-effort
        logger.warning("NewsAPI fetch failed: %s", exc)
        return []

    if data.get("status") != "ok":
        logger.warning("NewsAPI error: %s", data.get("message", "unknown"))
        return []

    candidates: list[Candidate] = []
    for art in data.get("articles", []):
        url = art.get("url") or ""
        title = (art.get("title") or "").strip()
        if not url or not title:
            continue
        stable_id = hashlib.sha256(url.encode()).hexdigest()[:16]
        source = (art.get("source") or {}).get("name") or "NewsAPI"
        candidates.append(
            Candidate(
                id=stable_id,
                title=title,
                body=(art.get("description") or "").strip(),
                url=url,
                lang=language or "",
                source=source,
                published_at=art.get("publishedAt") or "",
            )
        )
    return candidates
