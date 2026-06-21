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


def test_story_views_carry_furniture():
    doc = sample_render_document("economist")
    lead = doc.stories["s-lead"]
    assert lead.kicker == "В МИРЕ"
    assert lead.dateline == "ЖЕНЕВА"
    assert lead.kind == "feature"
    teaser = doc.stories["s-art"]
    assert teaser.kind == "teaser"
    assert teaser.teaser_text  # the "анонс" line
