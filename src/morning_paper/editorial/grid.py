from __future__ import annotations

import logging

from ..llm.client import AnthropicClient
from ..llm.models import OPUS
from ..models import GridPlan, GridSlot
from ..render.themes import ThemeManifest
from .summarize import SummarizedStory

logger = logging.getLogger(__name__)

GRID_SCHEMA = {
    "type": "object",
    "properties": {
        "section_order": {"type": "array", "items": {"type": "string"}},
        "slots": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "story_id": {"type": "string"},
                    "section": {"type": "string"},
                    "size": {"type": "string", "enum": ["lead", "medium", "brief"]},
                    "role": {
                        "type": "string",
                        "enum": ["feature", "standard", "brief", "teaser", "sidebar", "factbox"],
                    },
                    "dominant": {"type": "boolean"},
                    "body_policy": {"type": "string", "enum": ["full", "truncate", "teaser_only"]},
                    "row_span": {"type": "integer", "minimum": 1, "maximum": 4},
                    "front": {"type": "boolean"},
                    "columns": {"type": "integer", "minimum": 1, "maximum": 6},
                    "with_photo": {"type": "boolean"},
                    "pull_quote": {"type": ["string", "null"]},
                },
                "required": ["story_id", "section", "size", "columns", "with_photo"],
            },
        },
    },
    "required": ["section_order", "slots"],
}


def plan_grid(
    stories: list[SummarizedStory],
    *,
    theme: ThemeManifest,
    client: AnthropicClient | None = None,
) -> GridPlan:
    """Use Opus with extended thinking to decide grid layout. Returns validated GridPlan."""
    if not stories:
        return GridPlan()

    if client is None:
        client = AnthropicClient()

    story_list = "\n".join(
        f"- id={s.id} headline={s.headline!r}" for s in stories
    )
    system = (
        "You are a newspaper editor laying out a modular FRONT-PAGE MOSAIC. "
        "Pick ONE dominant lead (size=lead, role=feature, dominant=true, columns=all, front=true) "
        "as the Center of Visual Impact. Then TILE the page: stories' `columns` spans in each row "
        f"should sum to the page width ({theme.grid.columns} columns) — e.g. two half-width features, "
        "or a standard + a boxed sidebar, or a row of briefs/teasers. Mark short promos as role=teaser, "
        "body_policy=teaser_only ('анонс'). Set front=true for the ~6-8 stories that fill page one and "
        "front=false for the rest (they flow on later pages). Exactly one slot is dominant. "
        f"Respect: {theme.grid.columns} columns, max {theme.grid.max_lead} lead."
    )
    user_msg = (
        f"Plan a front-page mosaic for these {len(stories)} stories:\n{story_list}\n\n"
        "For each: section, size, role, dominant, body_policy, columns (span), front, "
        "and whether to show a photo. Make per-row column spans sum to the page width."
    )

    try:
        result = client.structured(
            [{"role": "user", "content": user_msg}],
            model=OPUS,
            system=system,
            schema=GRID_SCHEMA,
            tool_name="output",
            max_tokens=4096,
        )
        grid = GridPlan.model_validate(result)
        problems = grid.validate_against_theme(
            columns=theme.grid.columns, max_lead=theme.grid.max_lead
        )
        if problems:
            logger.warning("grid plan has constraint violations: %s; using fallback", problems)
            return _fallback_grid(stories, theme=theme)
        return grid
    except Exception as exc:
        logger.warning("plan_grid failed: %s; using fallback", exc)
        return _fallback_grid(stories, theme=theme)


def _fallback_grid(stories: list[SummarizedStory], *, theme: ThemeManifest) -> GridPlan:
    """Deterministic modular front-page mosaic + flow continuation when no LLM
    plans the page: a dominant lead feature (full bleed), rows of features and a
    standard+sidebar, a briefs/teasers row — tiled to fill page one — then the
    remaining stories flow on later pages."""
    cols = min(theme.grid.columns, 6)
    hi = (cols + 1) // 2          # ceil half
    lo = max(2, cols // 2)        # floor half (>=2)
    sm = 2
    n = len(stories)
    FRONT_MAX = 7                 # keep the mosaic to one page; rest is flow
    slots: list[GridSlot] = []

    for i, story in enumerate(stories):
        front = i < FRONT_MAX
        if i == 0:
            slot = GridSlot(story_id=story.id, section="world", size="lead", role="feature",
                            dominant=True, columns=cols, with_photo=True, front=True,
                            pull_quote=(story.deck or None))
        elif i in (1, 2):  # row: two features (lo + hi = cols)
            slot = GridSlot(story_id=story.id, section="world", size="medium", role="feature",
                            columns=(lo if i == 1 else hi), with_photo=(i == 1), front=front)
        elif i in (3, 4):  # row: standard + sidebar (lo + hi = cols)
            slot = GridSlot(story_id=story.id, section="world", size="medium",
                            role=("standard" if i == 3 else "sidebar"),
                            columns=(lo if i == 3 else hi), front=front)
        elif i in (5, 6):  # row: a brief + a teaser
            teaser = i == 6
            slot = GridSlot(story_id=story.id, section="world", size="brief",
                            role=("teaser" if teaser else "brief"),
                            body_policy=("teaser_only" if teaser else "full"),
                            columns=sm, front=front)
        else:              # flow continuation (pages 2+)
            teaser = i >= n - 2
            role = "teaser" if teaser else ("brief" if i % 3 == 0 else "standard")
            slot = GridSlot(story_id=story.id, section="world",
                            size=("brief" if role in ("brief", "teaser") else "medium"),
                            role=role, body_policy=("teaser_only" if teaser else "full"),
                            columns=(sm if role in ("brief", "teaser") else lo), front=False)
        slots.append(slot)

    return GridPlan(section_order=["world"], slots=slots)
