"""build_profile folds feedback into the profile (no-signals path needs no LLM)."""

from morning_paper.models import Feedback, InterestProfile
from morning_paper.profile.builder import build_profile


def test_feedback_applied_to_existing_profile_without_signals():
    existing = InterestProfile(user_id="u", topics={"ai": 1.0, "sport": 0.8})
    downvote = Feedback.make(user_id="u", vote=-1, topics=["sport"])
    out = build_profile("u", [], existing=existing, feedback=[downvote], output_lang="ru")
    # "sport" pushed down relative to "ai".
    assert out.topics["ai"] > out.topics.get("sport", 0.0)


def test_no_feedback_returns_existing_unchanged():
    existing = InterestProfile(user_id="u", topics={"ai": 1.0})
    out = build_profile("u", [], existing=existing, feedback=None)
    assert out.topics == {"ai": 1.0}


def test_empty_everything_yields_empty_profile():
    out = build_profile("u", [], existing=None, feedback=[])
    assert out.topics == {} and out.entities == {}
