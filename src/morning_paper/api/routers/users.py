"""User preferences (output language, theme, timezone, delivery channel)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from ... import accounts
from ..deps import Principal, get_principal, require_owner
from ..schemas import StyleOverrides, UserOut, UserUpdate

router = APIRouter(tags=["users"])


@router.get("/users/{user_id}/style")
def get_style(user_id: str, principal: Principal = Depends(get_principal)) -> dict:
    """The user's reading-comfort overrides (scale, leading, accent, fonts, dropcap)."""
    require_owner(principal, user_id)
    return accounts.load(user_id).style_overrides or {}


@router.put("/users/{user_id}/style")
def put_style(
    user_id: str, body: StyleOverrides, principal: Principal = Depends(get_principal)
) -> dict:
    """Merge in tuning overrides (only the provided keys change; null clears a key)."""
    require_owner(principal, user_id)
    acc = accounts.load(user_id)
    incoming = body.model_dump(exclude_unset=True)
    merged = dict(acc.style_overrides or {})
    for k, v in incoming.items():
        if v is None:
            merged.pop(k, None)
        else:
            merged[k] = v
    acc.style_overrides = merged
    accounts.save(acc)
    return merged


# --------------------------------------------------------------------------- #
# Privacy / data rights (GDPR/CCPA)
# --------------------------------------------------------------------------- #
@router.get("/users/{user_id}/data:export")
def export_data(user_id: str, principal: Principal = Depends(get_principal)) -> dict:
    """Export everything stored for the user (secrets redacted)."""
    require_owner(principal, user_id)
    from ... import privacy

    return privacy.export_user_data(user_id)


@router.delete("/users/{user_id}/data")
def delete_data(user_id: str, principal: Principal = Depends(get_principal)) -> dict:
    """Erase all stored data for the user (irreversible)."""
    require_owner(principal, user_id)
    from ... import privacy

    return privacy.delete_user_data(user_id)


def _to_out(acc: accounts.UserAccounts) -> UserOut:
    return UserOut(
        user_id=acc.user_id,
        output_lang=acc.output_lang,
        theme=acc.theme,
        tz=acc.tz,
        deliver_channel=acc.deliver_channel,
    )


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: str, principal: Principal = Depends(get_principal)) -> UserOut:
    require_owner(principal, user_id)
    return _to_out(accounts.load(user_id))


@router.put("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: str, body: UserUpdate, principal: Principal = Depends(get_principal)
) -> UserOut:
    require_owner(principal, user_id)
    acc = accounts.load(user_id)
    if body.output_lang is not None:
        acc.output_lang = body.output_lang
    if body.theme is not None:
        acc.theme = body.theme
    if body.tz is not None:
        acc.tz = body.tz
    if body.deliver_channel is not None:
        acc.deliver_channel = body.deliver_channel
    accounts.save(acc)

    try:  # best-effort mirror into the DB
        from ...db.repository import upsert_user

        upsert_user(
            user_id, tz=acc.tz, output_lang=acc.output_lang, default_theme=acc.theme
        )
    except Exception:
        pass

    return _to_out(acc)
