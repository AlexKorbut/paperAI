"""Phase: real-newspaper slot taxonomy — model + sample document wiring."""

from morning_paper.models import GridSlot
from morning_paper.sample import sample_render_document


def _slot(size, role=None):
    return GridSlot(story_id="a", section="s", size=size, columns=2, role=role)


def test_effective_role_falls_back_to_size():
    assert _slot("lead").effective_role == "feature"
    assert _slot("medium").effective_role == "standard"
    assert _slot("brief").effective_role == "brief"
    assert _slot("brief", role="teaser").effective_role == "teaser"


def test_sample_has_dominant_and_teaser_slots():
    doc = sample_render_document("times-classic")
    slots = doc.grid_plan.slots
    assert sum(1 for s in slots if s.dominant) == 1  # exactly one CVI
    teasers = [s for s in slots if s.effective_role == "teaser"]
    assert teasers and all(s.body_policy == "teaser_only" for s in teasers)
    assert any(s.effective_role == "sidebar" for s in slots)


def test_row_span_and_story_cols_defaults():
    s = _slot("medium")  # columns=2
    assert s.row_span == 1 and s.front is True
    assert s.effective_story_cols == 1  # standard, span 2 -> 1 text column
    dom = GridSlot(story_id="a", section="s", size="lead", columns=6, dominant=True)
    assert dom.effective_story_cols == 3  # 6//2
    assert GridSlot(story_id="a", section="s", size="brief", columns=2, role="teaser").effective_story_cols == 1


def test_front_mosaic_tiles_and_has_flow():
    # times-classic is 6 columns: dominant spans all; front rows tile to 6.
    doc = sample_render_document("times-classic")
    front = [s for s in doc.grid_plan.slots if s.front]
    assert any(s.dominant and s.columns == 6 for s in front)
    # the two-feature row sums to the page width
    assert sum(s.columns for s in front if s.story_id in ("s-eu", "s-mkt")) == 6


def test_story_views_carry_furniture():
    doc = sample_render_document("economist")
    lead = doc.stories["s-lead"]
    assert lead.kicker == "В МИРЕ"
    assert lead.dateline == "ЖЕНЕВА"
    assert lead.kind == "feature"
    teaser = doc.stories["s-art"]
    assert teaser.kind == "teaser"
    assert teaser.teaser_text  # the "анонс" line
