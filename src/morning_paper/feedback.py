"""Feedback loop: in-product 👍/👎 folded back into the interest profile.

This is the learning mechanism of v1 — the more a user reacts to stories, the
better the profile tracks their taste. Feedback is stored file-backed (like
``accounts``) so it works with zero infrastructure, and applied as a signed,
recency-weighted nudge to the profile's topic/entity weights.

Only labels (topics/entities/section) are stored — never article text — so the
privacy invariant from docs/03 holds here too.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .models import Feedback, InterestProfile


def _dir() -> Path:
    """Feedback store dir, a sibling of the per-user accounts dir."""
    from .accounts import _users_dir

    d = _users_dir().parent / "feedback"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _path(user_id: str) -> Path:
    return _dir() / f"{user_id.replace('/', '_')}.json"


def record(fb: Feedback) -> None:
    """Append one feedback event for a user."""
    p = _path(fb.user_id)
    events = load(fb.user_id)
    events.append(fb)
    p.write_text(
        json.dumps([e.model_dump(mode="json") for e in events], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load(user_id: str) -> list[Feedback]:
    """All stored feedback for a user (oldest first); ``[]`` if none."""
    p = _path(user_id)
    if not p.exists():
        return []
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return [Feedback.model_validate(item) for item in raw]


def clear(user_id: str) -> int:
    """Delete a user's feedback file; return how many events were removed."""
    p = _path(user_id)
    if not p.exists():
        return 0
    n = len(load(user_id))
    p.unlink()
    return n


# --------------------------------------------------------------------------- #
# Applying feedback to a profile
# --------------------------------------------------------------------------- #
def apply_to_profile(
    profile: InterestProfile,
    events: list[Feedback],
    *,
    learning_rate: float = 0.2,
    halflife_days: float = 14.0,
) -> InterestProfile:
    """Return a copy of ``profile`` nudged by feedback.

    Each event shifts its topics/entities by ``vote * learning_rate``, decayed by
    recency (older feedback counts less). Weights are clamped to [0, 1]; anything
    driven to zero (e.g. by repeated 👎) is dropped; the result is renormalized so
    the strongest interest sits at 1.0 — matching the aggregator's convention.
    """
    if not events:
        return profile

    topics = dict(profile.topics)
    entities = dict(profile.entities)
    now = datetime.now(timezone.utc)

    for fb in events:
        delta = fb.vote * learning_rate * _recency(fb.created_at, now, halflife_days)
        for topic in fb.topics:
            t = topic.strip()
            if t:
                topics[t] = _clamp(topics.get(t, 0.0) + delta)
        for entity in fb.entities:
            e = entity.strip()
            if e:
                entities[e] = _clamp(entities.get(e, 0.0) + delta)

    return profile.model_copy(
        update={
            "topics": _normalize(_drop_nonpositive(topics)),
            "entities": _normalize(_drop_nonpositive(entities)),
            "updated_at": now,
            "version": profile.version + 1,
        }
    )


def _recency(created_at: datetime, now: datetime, halflife_days: float) -> float:
    try:
        age_days = max(0.0, (now - created_at).total_seconds() / 86400.0)
    except (TypeError, ValueError):
        return 1.0
    if halflife_days <= 0:
        return 1.0
    return 0.5 ** (age_days / halflife_days)


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def _drop_nonpositive(scores: dict[str, float]) -> dict[str, float]:
    return {k: v for k, v in scores.items() if v > 0.0}


def _normalize(scores: dict[str, float]) -> dict[str, float]:
    if not scores:
        return scores
    max_val = max(scores.values())
    if max_val <= 0.0:
        return scores
    return {k: v / max_val for k, v in scores.items()}
