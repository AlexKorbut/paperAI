"""Print order service: quote, create+submit, and a file-backed order store."""

from __future__ import annotations

import json
import re
from pathlib import Path

from ..models import PrintAddress, PrintOrder, PrintQuote
from .base import get_provider, list_providers

_PAGE_RE = re.compile(rb"/Type\s*/Page(?![s])")


def available_providers() -> list[dict]:
    """Provider catalog for the UI: id, name, formats."""
    return [
        {
            "provider_id": p.provider_id,
            "display_name": p.display_name,
            "supported_formats": list(p.supported_formats),
            "min_total_usd": p.min_total_usd,
        }
        for p in list_providers()
    ]


def quote(provider_id: str, *, format: str, pages: int, copies: int, country: str = "US") -> PrintQuote:
    return get_provider(provider_id).quote(format=format, pages=pages, copies=copies, country=country)


def count_pdf_pages(pdf_path: str | Path, *, default: int = 4) -> int:
    """Best-effort page count for one of our generated PDFs.

    Counts ``/Type /Page`` markers (excluding ``/Pages``). Falls back to
    ``default`` if the file is missing/unreadable or nothing matches.
    """
    try:
        data = Path(pdf_path).read_bytes()
    except OSError:
        return default
    n = len(_PAGE_RE.findall(data))
    return n if n > 0 else default


def _provider_api_key(provider_id: str) -> str | None:
    try:
        from ..config import get_settings

        secrets = get_settings().secrets
        return {
            "newspaper_club": secrets.newspaper_club_api_key,
            "mixam": secrets.mixam_api_key,
        }.get(provider_id)
    except Exception:
        return None


def create_order(
    user_id: str,
    *,
    provider_id: str,
    format: str,
    copies: int,
    address: PrintAddress,
    issue_id: str | None = None,
    pages: int | None = None,
    pdf_path: str | Path | None = None,
    country: str | None = None,
    submit: bool = True,
) -> PrintOrder:
    """Quote, build, (optionally) submit, and persist a print order."""
    provider = get_provider(provider_id)
    resolved_pages = pages if pages is not None else (
        count_pdf_pages(pdf_path) if pdf_path else 4
    )
    q = provider.quote(
        format=format,
        pages=resolved_pages,
        copies=copies,
        country=country or address.country,
    )
    order = PrintOrder.make(
        user_id=user_id, provider=provider_id, quote=q, address=address,
        copies=copies, issue_id=issue_id,
    )
    order.status = "quoted"
    if submit:
        order = provider.submit(
            order,
            pdf_path=Path(pdf_path) if pdf_path else None,
            api_key=_provider_api_key(provider_id),
        )
    _record(order)
    return order


# --------------------------------------------------------------------------- #
# File-backed order store (a sibling of accounts/feedback)
# --------------------------------------------------------------------------- #
def _dir() -> Path:
    from ..accounts import _users_dir

    d = _users_dir().parent / "print_orders"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _path(user_id: str) -> Path:
    return _dir() / f"{user_id.replace('/', '_')}.json"


def _record(order: PrintOrder) -> None:
    orders = list_orders(order.user_id)
    orders.append(order)
    _path(order.user_id).write_text(
        json.dumps([o.model_dump(mode="json") for o in orders], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def list_orders(user_id: str) -> list[PrintOrder]:
    p = _path(user_id)
    if not p.exists():
        return []
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return [PrintOrder.model_validate(item) for item in raw]


def load_order(user_id: str, order_id: str) -> PrintOrder | None:
    for o in list_orders(user_id):
        if o.id == order_id:
            return o
    return None
