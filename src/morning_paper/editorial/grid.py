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
        "You are a newspaper editor planning a front page with real hierarchy. "
        "Pick ONE dominant lead story (size=lead, role=feature, dominant=true) as the "
        "Center of Visual Impact. Give the next 1-2 stories role=feature; make a few "
        "role=standard; cluster the shortest as role=brief; mark 1-2 short items as "
        "role=teaser with body_policy=teaser_only (an 'анонс' pointing inside). Use "
        "role=sidebar for a boxed companion when relevant. Exactly one slot may be dominant. "
        f"Respect the theme constraints: {theme.grid.columns} columns, "
        f"max {theme.grid.max_lead} lead stories."
    )
    user_msg = (
        f"Plan a grid layout for these {len(stories)} stories:\n{story_list}\n\n"
        "For each story assign: section, size (lead/medium/brief), role, dominant, "
        "body_policy, column span, and whether to show a photo."
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
    """Deterministic newspaper hierarchy when no LLM plans the page:
    one dominant lead feature, a couple of features, standards, a briefs cluster,
    and 1-2 teasers ("анонсы") at the tail."""
    cols = theme.grid.columns
    mid = max(2, min(cols, 3))
    small = max(2, min(cols, 6) // 2)
    n = len(stories)
    slots: list[GridSlot] = []

    for i, story in enumerate(stories):
        if i == 0:
            slot = GridSlot(story_id=story.id, section="world", size="lead",
                            role="feature", dominant=True, columns=min(cols, 6), with_photo=True,
                            pull_quote=(story.deck or None))
        elif i == 1:
            slot = GridSlot(story_id=story.id, section="world", size="medium",
                            role="feature", columns=mid, with_photo=True)
        elif n > 5 and i >= n - 2:
            # tail items become teasers / анонсы
            slot = GridSlot(story_id=story.id, section="world", size="brief",
                            role="teaser", body_policy="teaser_only", columns=small)
        elif i % 4 == 0:
            slot = GridSlot(story_id=story.id, section="world", size="brief",
                            role="brief", columns=small)
        else:
            slot = GridSlot(story_id=story.id, section="world", size="medium",
                            role="standard", columns=mid)
        slots.append(slot)

    return GridPlan(section_order=["world"], slots=slots)
