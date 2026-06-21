"""Theme marketplace listing (read-only over HTTP).

Installing third-party themes writes to the server's theme directory, so it is
intentionally a CLI/operator action (`morning-paper install-theme`), not an API
endpoint that accepts arbitrary uploads.
"""

from __future__ import annotations

from fastapi import APIRouter

from ..schemas import MarketplaceTheme

router = APIRouter(tags=["marketplace"])


@router.get("/marketplace/themes", response_model=list[MarketplaceTheme])
def marketplace_themes() -> list[MarketplaceTheme]:
    from ... import marketplace

    return [MarketplaceTheme(**item) for item in marketplace.listing()]
