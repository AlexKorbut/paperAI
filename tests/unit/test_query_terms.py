from morning_paper.models import InterestProfile
from morning_paper.retrieval.query import profile_query_terms


def _profile(topics=None, entities=None) -> InterestProfile:
    return InterestProfile(
        user_id="u",
        topics=topics or {},
        entities=entities or {},
    )


def test_entities_lead_then_topic_leaves_by_weight():
    p = _profile(
        topics={"технологии/ИИ": 0.9, "спорт/велоспорт": 0.3},
        entities={"Anthropic": 0.8, "Tour de France": 0.2},
    )
    terms = profile_query_terms(p, max_terms=8)
    # Entities first (by weight), then topic leaves (by weight).
    assert terms == ["Anthropic", "Tour de France", "ИИ", "велоспорт"]


def test_dedup_case_insensitive_and_cap():
    p = _profile(
        topics={"a/ИИ": 0.5, "b/ии": 0.4, "c/space": 0.3},
        entities={"ИИ": 0.9},
    )
    terms = profile_query_terms(p, max_terms=2)
    assert terms == ["ИИ", "space"]  # entity ИИ wins, topic ИИ/ии de-duped, capped at 2


def test_empty_profile_yields_no_terms():
    assert profile_query_terms(_profile()) == []
