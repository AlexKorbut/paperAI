from datetime import datetime, timedelta, timezone

from morning_paper import feedback as fb
from morning_paper.models import Feedback, InterestProfile


def _fb(user="u", vote=1, topics=None, entities=None, created_at=None) -> Feedback:
    return Feedback(
        id=f"{vote}-{topics}-{created_at}",
        user_id=user,
        vote=vote,
        topics=topics or [],
        entities=entities or [],
        created_at=created_at or datetime.now(timezone.utc),
    )


def test_make_normalizes_vote():
    assert Feedback.make(user_id="u", vote=5).vote == 1
    assert Feedback.make(user_id="u", vote=-3).vote == -1


def test_upvote_boosts_topic():
    p = InterestProfile(user_id="u", topics={"a": 0.5, "b": 0.5})
    out = fb.apply_to_profile(p, [_fb(topics=["a"])])
    assert out.topics["a"] > out.topics["b"]
    assert out.version == p.version + 1


def test_downvote_suppresses_and_can_drop_topic():
    p = InterestProfile(user_id="u", topics={"a": 0.1, "b": 1.0})
    out = fb.apply_to_profile(p, [_fb(vote=-1, topics=["a"])], learning_rate=0.2)
    # 0.1 - 0.2 -> clamped to 0 -> dropped entirely.
    assert "a" not in out.topics
    assert "b" in out.topics


def test_entities_are_nudged_too():
    p = InterestProfile(user_id="u", entities={"Anthropic": 0.5})
    out = fb.apply_to_profile(p, [_fb(entities=["Anthropic"])])
    assert out.entities["Anthropic"] == 1.0  # normalized to max


def test_recency_decay_weakens_old_feedback():
    p = InterestProfile(user_id="u", topics={"a": 0.5, "b": 0.5})
    old = _fb(topics=["b"], created_at=datetime.now(timezone.utc) - timedelta(days=28))
    recent = _fb(topics=["a"], created_at=datetime.now(timezone.utc))
    out = fb.apply_to_profile(p, [old, recent], learning_rate=0.2, halflife_days=14.0)
    # recent upvote on "a" should outrank the decayed upvote on "b".
    assert out.topics["a"] > out.topics["b"]


def test_no_events_returns_same_profile():
    p = InterestProfile(user_id="u", topics={"a": 1.0})
    assert fb.apply_to_profile(p, []) is p


def test_record_load_clear_roundtrip():
    fb.record(Feedback.make(user_id="alice", vote=1, topics=["tech"], story_id="s1"))
    fb.record(Feedback.make(user_id="alice", vote=-1, entities=["X"], story_id="s2"))
    events = fb.load("alice")
    assert len(events) == 2
    assert events[0].story_id == "s1" and events[0].vote == 1
    assert events[1].vote == -1

    removed = fb.clear("alice")
    assert removed == 2
    assert fb.load("alice") == []


def test_load_unknown_user_is_empty():
    assert fb.load("nobody") == []
