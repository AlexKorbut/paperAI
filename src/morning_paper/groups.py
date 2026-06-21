"""Family / team groups (Phase 3): one shared paper for several people.

A group is a named set of member user-ids with its own style/language. Its
issue is built from a *merged* interest profile — the union of members' topics,
entities and interest vectors — so one paper reflects everyone, then it is
delivered to each member's channel.

Stored file-backed (like accounts/feedback) so it works with zero infra.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import Group, InterestProfile


def _dir() -> Path:
    from .accounts import _users_dir

    d = _users_dir().parent / "groups"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _path(group_id: str) -> Path:
    return _dir() / f"{group_id}.json"


def save(group: Group) -> None:
    _path(group.id).write_text(group.model_dump_json(indent=2), encoding="utf-8")


def load(group_id: str) -> Group | None:
    p = _path(group_id)
    if not p.exists():
        return None
    return Group.model_validate_json(p.read_text(encoding="utf-8"))


def create(name: str, owner: str, *, members: list[str] | None = None,
           theme: str | None = None, output_lang: str | None = None) -> Group:
    g = Group.make(name=name, owner=owner, members=members, theme=theme, output_lang=output_lang)
    save(g)
    return g


def delete(group_id: str) -> bool:
    p = _path(group_id)
    if p.exists():
        p.unlink()
        return True
    return False


def list_groups(owner: str | None = None) -> list[Group]:
    out: list[Group] = []
    for f in sorted(_dir().glob("*.json")):
        try:
            g = Group.model_validate_json(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if owner is None or g.owner == owner:
            out.append(g)
    return out


def add_member(group_id: str, user_id: str) -> Group:
    g = load(group_id)
    if g is None:
        raise KeyError(f"no group {group_id!r}")
    if user_id not in g.members:
        g.members.append(user_id)
        save(g)
    return g


def remove_member(group_id: str, user_id: str) -> Group:
    g = load(group_id)
    if g is None:
        raise KeyError(f"no group {group_id!r}")
    if user_id == g.owner:
        raise ValueError("cannot remove the group owner")
    g.members = [m for m in g.members if m != user_id]
    save(g)
    return g


# --------------------------------------------------------------------------- #
# Merged profile
# --------------------------------------------------------------------------- #
def _load_member_profile(user_id: str) -> InterestProfile | None:
    try:
        from .db.repository import load_profile

        return load_profile(user_id)
    except Exception:
        return None


def aggregate_group_profile(
    group: Group,
    *,
    profiles: dict[str, InterestProfile] | None = None,
) -> InterestProfile:
    """Merge members' profiles into one. Topic/entity weights are summed then
    renormalized (a shared interest reinforces); interest vectors are unioned
    (capped). ``profiles`` may be injected (tests); otherwise loaded per member.
    """
    topics: dict[str, float] = {}
    entities: dict[str, float] = {}
    vectors: list[list[float]] = []

    for uid in group.members:
        prof = (profiles or {}).get(uid) if profiles is not None else _load_member_profile(uid)
        if prof is None:
            continue
        for t, w in prof.topics.items():
            topics[t] = topics.get(t, 0.0) + w
        for e, w in prof.entities.items():
            entities[e] = entities.get(e, 0.0) + w
        vectors.extend(prof.interest_vectors)

    return InterestProfile(
        user_id=group.id,
        output_lang=group.output_lang or "ru",
        topics=_normalize(topics),
        entities=_normalize(entities),
        interest_vectors=vectors[:24],
    )


def _normalize(scores: dict[str, float]) -> dict[str, float]:
    if not scores:
        return scores
    m = max(scores.values())
    return {k: v / m for k, v in scores.items()} if m > 0 else scores


# --------------------------------------------------------------------------- #
# Group issue: build once from the merged profile, deliver to every member
# --------------------------------------------------------------------------- #
def run_group_issue(
    group_id: str,
    *,
    theme_id: str | None = None,
    output_lang: str | None = None,
    out_dir: Path | None = None,
) -> dict:
    """Build one issue for the group and fan it out to members' channels.

    Returns {group_id, issue_id, pdf_path, deliveries:[{user_id, channel, ok}]}.
    """
    from . import accounts
    from .delivery import get_deliverer
    from .pipeline.run import run_issue

    group = load(group_id)
    if group is None:
        raise KeyError(f"no group {group_id!r}")

    merged = aggregate_group_profile(group)

    # Render only (stage <=7); we handle multi-member delivery ourselves.
    ctx = run_issue(
        group.id,
        theme_id=theme_id or group.theme,
        output_lang=output_lang or group.output_lang,
        out_dir=out_dir,
        seed_profile=merged,
        until_stage=7,
    )

    deliveries: list[dict] = []
    if ctx.pdf_path:
        for uid in group.members:
            channel = accounts.load(uid).deliver_channel or "file"
            try:
                deliverer = get_deliverer(channel)
                res = deliverer.deliver(
                    ctx.pdf_path,
                    user_id=uid,
                    subject=f"{group.name} — {ctx.issue_id}",
                    body="Ваш общий выпуск готов.",
                )
                deliveries.append({"user_id": uid, "channel": channel, "ok": bool(res.ok)})
            except Exception:
                deliveries.append({"user_id": uid, "channel": channel, "ok": False})

    return {
        "group_id": group.id,
        "issue_id": ctx.issue_id,
        "pdf_path": str(ctx.pdf_path) if ctx.pdf_path else None,
        "deliveries": deliveries,
    }
