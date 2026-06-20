"""GDELT DOC 2.0 retriever — free, key-less, multilingual candidate news.

GDELT indexes worldwide news in many languages; we query its ArtList mode with
terms derived from the user's interest profile. Articles come back as title +
url + metadata (no body), which is enough for ranking and for the editorial
stage to summarise/translate. Failures are swallowed by the caller (the stage
logs a warning and continues with whatever other sources returned).
"""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone

import httpx

from .feeds import Candidate

logger = logging.getLogger(__name__)

GDELT_DOC_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def build_gdelt_query(terms: list[str], *, source_langs: list[str] | None = None) -> str:
    """Format profile terms into a GDELT query string.

    Multi-word terms are quoted as phrases; multiple terms are OR-ed so a story
    matching any interest is a candidate. An optional language filter is AND-ed
    on top (e.g. restrict to English/Russian source language).
    """
    quoted = [f'"{t}"' if " " in t else t for t in terms if t.strip()]
    if not quoted:
        return ""
    query = "(" + " OR ".join(quoted) + ")" if len(quoted) > 1 else quoted[0]

    langs = [lang for lang in (source_langs or []) if lang.strip()]
    if langs:
        lang_clause = (
            "(" + " OR ".join(f"sourcelang:{lang}" for lang in langs) + ")"
            if len(langs) > 1
            else f"sourcelang:{langs[0]}"
        )
        query = f"{query} {lang_clause}"
    return query


def fetch_gdelt_candidates(
    terms: list[str],
    *,
    max_records: int = 75,
    timespan: str = "1d",
    source_langs: list[str] | None = None,
    timeout: float = 30.0,
) -> list[Candidate]:
    """Query GDELT for recent articles matching the profile terms."""
    query = build_gdelt_query(terms, source_langs=source_langs)
    if not query:
        return []

    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": str(max(1, min(max_records, 250))),
        "timespan": timespan,
        "sort": "DateDesc",
    }
    try:
        resp = httpx.get(GDELT_DOC_URL, params=params, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:  # noqa: BLE001 - retrieval is best-effort
        logger.warning("GDELT fetch failed: %s", exc)
        return []

    candidates: list[Candidate] = []
    for art in data.get("articles", []):
        url = art.get("url") or ""
        title = (art.get("title") or "").strip()
        if not url or not title:
            continue
        stable_id = hashlib.sha256(url.encode()).hexdigest()[:16]
        candidates.append(
            Candidate(
                id=stable_id,
                title=title,
                body="",  # ArtList carries no body; editorial works from the title + url
                url=url,
                lang=(art.get("language") or "").strip(),
                source=art.get("domain") or "GDELT",
                published_at=_gdelt_iso(art.get("seendate")),
            )
        )
    return candidates


def _gdelt_iso(seendate: str | None) -> str:
    """Convert GDELT's ``20260619T120000Z`` timestamp to ISO-8601."""
    if not seendate:
        return ""
    try:
        dt = datetime.strptime(seendate, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        return dt.isoformat()
    except (ValueError, TypeError):
        return ""
