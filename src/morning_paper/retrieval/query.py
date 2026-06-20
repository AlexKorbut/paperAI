"""Turn an InterestProfile into search terms for external news APIs.

Topics are stored as taxonomy paths (e.g. ``технологии/ИИ``); for a free-text
search we want the most specific, highest-signal leaves plus named entities,
ordered by weight. Each retriever formats these terms into its own query
dialect (GDELT vs NewsAPI), so this module only produces the ordered term list.
"""

from __future__ import annotations

from ..models import InterestProfile


def _leaf(topic_path: str) -> str:
    """Last segment of a taxonomy path: ``геополитика/Ближний Восток`` -> that tail."""
    return topic_path.rsplit("/", 1)[-1].strip()


def profile_query_terms(profile: InterestProfile, *, max_terms: int = 8) -> list[str]:
    """Ordered, de-duplicated search terms from a profile (entities first).

    Entities (concrete people/orgs/places) are the strongest, most precise
    signal, so they lead; topic leaves follow. Both are sorted by weight.
    """
    terms: list[str] = []
    seen: set[str] = set()

    def add(raw: str) -> None:
        term = raw.strip()
        key = term.lower()
        if term and key not in seen:
            seen.add(key)
            terms.append(term)

    for entity, _w in sorted(profile.entities.items(), key=lambda kv: kv[1], reverse=True):
        add(entity)
    for topic, _w in sorted(profile.topics.items(), key=lambda kv: kv[1], reverse=True):
        add(_leaf(topic))

    return terms[:max_terms]
