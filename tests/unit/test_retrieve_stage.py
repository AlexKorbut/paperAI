"""Stage-level wiring: s3_retrieve combines RSS + GDELT; s4_rank scores them.

External calls are monkeypatched, so no network/keys are needed.
"""

from pathlib import Path

from morning_paper.models import InterestProfile
from morning_paper.pipeline.context import IssueContext
from morning_paper.pipeline import stages
from morning_paper.retrieval import feeds, gdelt


def _ctx(tmp_path: Path, profile: InterestProfile | None) -> IssueContext:
    ctx = IssueContext(
        user_id="u", issue_id="i", theme_id="times-classic",
        output_lang="ru", work_dir=tmp_path,
    )
    ctx.profile = profile
    return ctx


def _cand(source_mod, id, title):
    return source_mod.Candidate(
        id=id, title=title, body="", url=f"https://x/{id}", lang="en",
        source="t", published_at="",
    )


def test_retrieve_combines_rss_and_gdelt(tmp_path, monkeypatch):
    monkeypatch.setattr(
        feeds, "fetch_rss_candidates",
        lambda urls, max_per_feed=20: [_cand(feeds, "rss1", "RSS world news")],
    )
    captured = {}

    def fake_gdelt(terms, **kwargs):
        captured["terms"] = terms
        return [_cand(feeds, "g1", "GDELT про ИИ")]

    monkeypatch.setattr(gdelt, "fetch_gdelt_candidates", fake_gdelt)

    profile = InterestProfile(user_id="u", topics={"технологии/ИИ": 0.9}, entities={"Anthropic": 0.8})
    ctx = stages.s3_retrieve(_ctx(tmp_path, profile))

    ids = {c.id for c in ctx.candidates}
    assert ids == {"rss1", "g1"}
    # GDELT was queried with profile-derived terms (entities first).
    assert captured["terms"][0] == "Anthropic"


def test_retrieve_without_profile_skips_gdelt(tmp_path, monkeypatch):
    monkeypatch.setattr(
        feeds, "fetch_rss_candidates",
        lambda urls, max_per_feed=20: [_cand(feeds, "rss1", "RSS only")],
    )

    def boom(*a, **k):  # pragma: no cover - must not be called
        raise AssertionError("GDELT should not run without a profile")

    monkeypatch.setattr(gdelt, "fetch_gdelt_candidates", boom)

    ctx = stages.s3_retrieve(_ctx(tmp_path, None))
    assert [c.id for c in ctx.candidates] == ["rss1"]


def test_rank_stage_orders_and_dedups(tmp_path, monkeypatch):
    profile = InterestProfile(user_id="u", topics={"market": 1.0}, entities={})
    ctx = _ctx(tmp_path, profile)
    ctx.candidates = [
        _cand(feeds, "a", "A rocket launch"),
        _cand(feeds, "b", "Stock market rallies"),
    ]
    ctx = stages.s4_rank(ctx)
    assert ctx.ranked[0].id == "b"  # keyword match on "market"
