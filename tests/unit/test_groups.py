from types import SimpleNamespace

import pytest

from morning_paper import groups
from morning_paper.models import InterestProfile


def test_create_includes_owner_and_dedups():
    g = groups.create("Family", owner="dad", members=["mom", "dad", "kid"])
    assert g.owner == "dad"
    assert g.members == ["dad", "mom", "kid"]  # owner first, de-duped
    assert groups.load(g.id) is not None


def test_membership_ops_and_owner_protection():
    g = groups.create("Team", owner="lead", members=["a"])
    g = groups.add_member(g.id, "b")
    assert set(g.members) == {"lead", "a", "b"}
    g = groups.remove_member(g.id, "a")
    assert "a" not in g.members
    with pytest.raises(ValueError):
        groups.remove_member(g.id, "lead")


def test_list_groups_filters_by_owner():
    groups.create("G1", owner="x")
    groups.create("G2", owner="y")
    assert {g.name for g in groups.list_groups(owner="x")} == {"G1"}
    assert len(groups.list_groups()) >= 2


def test_delete_group():
    g = groups.create("Temp", owner="z")
    assert groups.delete(g.id) is True
    assert groups.load(g.id) is None


def test_aggregate_group_profile_merges_and_normalizes():
    g = groups.create("Fam", owner="p1", members=["p2"])
    profiles = {
        "p1": InterestProfile(user_id="p1", topics={"ai": 1.0, "sport": 0.5}, entities={"NASA": 0.4},
                              interest_vectors=[[1.0, 0.0]]),
        "p2": InterestProfile(user_id="p2", topics={"ai": 0.5, "music": 1.0}, entities={"NASA": 0.6},
                              interest_vectors=[[0.0, 1.0]]),
    }
    merged = groups.aggregate_group_profile(g, profiles=profiles)
    # ai summed (1.5) is the max -> normalized to 1.0; music 1.0/1.5; sport 0.5/1.5
    assert merged.topics["ai"] == pytest.approx(1.0)
    assert merged.topics["music"] == pytest.approx(1.0 / 1.5)
    assert merged.entities["NASA"] == pytest.approx(1.0)  # summed 1.0 then normalized
    assert len(merged.interest_vectors) == 2
    assert merged.user_id == g.id


def test_run_group_issue_fans_out(monkeypatch):
    g = groups.create("Fam", owner="a", members=["b"])

    # Fake the pipeline render: return a ctx carrying a pdf path + issue id.
    fake_pdf = "/tmp/whatever.pdf"
    captured = {}

    def fake_run_issue(user_id, *, seed_profile=None, until_stage=8, **kw):
        captured["user_id"] = user_id
        captured["seeded"] = seed_profile is not None
        captured["until_stage"] = until_stage
        return SimpleNamespace(pdf_path=fake_pdf, issue_id="grp-iss-1", theme_id="economist")

    delivered: list[str] = []

    class FakeDeliverer:
        def deliver(self, pdf_path, *, user_id, subject, body="", **kw):
            delivered.append(user_id)
            return SimpleNamespace(ok=True, channel="file")

    import morning_paper.pipeline.run as run_mod
    import morning_paper.delivery as deliv_mod

    monkeypatch.setattr(run_mod, "run_issue", fake_run_issue)
    monkeypatch.setattr(deliv_mod, "get_deliverer", lambda channel="file", **kw: FakeDeliverer())

    result = groups.run_group_issue(g.id, theme_id="economist")
    assert result["issue_id"] == "grp-iss-1"
    assert captured["user_id"] == g.id
    assert captured["seeded"] is True
    assert captured["until_stage"] == 7
    assert set(delivered) == {"a", "b"}
    assert all(d["ok"] for d in result["deliveries"])
