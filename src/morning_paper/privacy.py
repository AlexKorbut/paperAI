"""GDPR/CCPA data rights: export and delete everything we hold for a user.

The product's privacy stance (docs/03, docs/07) is that a user can see and erase
their data on request. This module gathers the file-backed stores (accounts,
feedback) and the optional DB rows (profile, signals, issues) into one export,
and deletes them. Secrets (session strings, tokens) are redacted from exports —
they are credentials, not user data, and must never leave the server.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from . import accounts, feedback
from .api.schemas import redact_options


def export_user_data(user_id: str) -> dict:
    """Assemble a JSON-able snapshot of everything stored for ``user_id``.

    Never includes secrets or raw private signal text (the latter is never stored
    in the first place).
    """
    acc = accounts.load(user_id)
    sources = {
        sid: {
            "enabled": sa.enabled,
            "status": sa.status,
            "options": redact_options(sa.options),
            "has_secret": sa.secret_ref is not None,
        }
        for sid, sa in acc.sources.items()
    }

    export: dict = {
        "user_id": user_id,
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "preferences": {
            "output_lang": acc.output_lang,
            "theme": acc.theme,
            "tz": acc.tz,
            "deliver_channel": acc.deliver_channel,
        },
        "sources": sources,
        "feedback": [fb.model_dump(mode="json") for fb in feedback.load(user_id)],
        "profile": _export_profile(user_id),
        "issues": _export_issues(user_id),
    }
    return export


def delete_user_data(user_id: str) -> dict:
    """Erase all stored data for a user. Returns a summary of what was removed."""
    removed: dict[str, int | bool] = {}

    acc_path = accounts._path(user_id)
    removed["accounts"] = acc_path.exists()
    acc_path.unlink(missing_ok=True)

    removed["feedback_events"] = feedback.clear(user_id)

    try:
        from .db.repository import delete_user as _delete_user

        removed["db_rows"] = _delete_user(user_id)
    except Exception:
        removed["db_rows"] = 0

    return {"user_id": user_id, "removed": removed}


def _export_profile(user_id: str) -> dict | None:
    try:
        from .db.repository import load_profile

        profile = load_profile(user_id)
    except Exception:
        profile = None
    if profile is None:
        return None
    return {
        "output_lang": profile.output_lang,
        "topics": dict(profile.topics),
        "entities": dict(profile.entities),
        "interest_vector_count": len(profile.interest_vectors),
        "version": profile.version,
        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
    }


def _export_issues(user_id: str) -> list[dict]:
    try:
        from .db.repository import list_user_issues

        return list_user_issues(user_id)
    except Exception:
        return []


def write_export(user_id: str, out_path: Path) -> Path:
    """Convenience: export and write to a JSON file."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(export_user_data(user_id), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path
