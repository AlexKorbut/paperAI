"""Theme catalog. Exposes only safe public fields (no font files/licenses)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse

from ...render.themes import list_manifests
from ..schemas import ThemeOut

router = APIRouter(tags=["themes"])


@router.get("/themes/{theme_id}/preview", response_class=HTMLResponse)
def theme_preview(
    theme_id: str,
    scale: float | None = Query(default=None),
    leading: float | None = Query(default=None),
    accent: str | None = Query(default=None),
    body_font: str | None = Query(default=None),
    headline_font: str | None = Query(default=None),
    dropcap: bool | None = Query(default=None),
    locale: str = Query(default="ru"),
) -> HTMLResponse:
    """Self-contained HTML specimen of a theme (live, honours tuning query params).

    Embedded in an <iframe> by the cabinet so the user sees the real fonts +
    layout style, updating as they drag the tuning sliders.
    """
    from ...render.renderer import NodeRenderer, RenderError
    from ...sample import specimen_render_document

    overrides = {
        k: v
        for k, v in {
            "scale": scale, "leading": leading, "accent": accent,
            "body_font": body_font, "headline_font": headline_font, "dropcap": dropcap,
        }.items()
        if v is not None
    }
    try:
        doc = specimen_render_document(theme_id, locale=locale, style_overrides=overrides)
    except FileNotFoundError:
        raise HTTPException(404, f"no theme {theme_id!r}")
    try:
        html = NodeRenderer().web_html(doc)
    except RenderError as e:
        raise HTTPException(503, f"preview unavailable: {e}")
    return HTMLResponse(content=html)


@router.get("/themes", response_model=list[ThemeOut])
def list_themes() -> list[ThemeOut]:
    out: list[ThemeOut] = []
    for m in list_manifests():
        out.append(
            ThemeOut(
                id=m.id,
                display_name=m.display_name,
                mood=m.mood,
                page=m.format.page,
                columns=m.grid.columns,
                color_mode=m.format.color_mode,
                colors={
                    "paper": m.colors.paper,
                    "ink": m.colors.ink,
                    "accent": m.colors.accent,
                },
                author=m.marketplace.author,
                price_usd=m.marketplace.price_usd,
            )
        )
    return out
