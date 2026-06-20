from morning_paper import accounts, feedback, privacy
from morning_paper.models import Feedback


def _setup_user(user="bob"):
    acc = accounts.load(user)
    acc.theme = "economist"
    acc.output_lang = "en"
    accounts.save(acc)
    accounts.set_source(
        user,
        "telegram",
        options={"channel": "@news", "session_string": "TOPSECRET"},
        secret_ref="vault://bob/tg",
    )
    feedback.record(Feedback.make(user_id=user, vote=1, topics=["tech"], story_id="s1"))


def test_export_includes_prefs_sources_feedback_and_redacts_secrets():
    _setup_user()
    data = privacy.export_user_data("bob")

    assert data["preferences"]["theme"] == "economist"
    assert data["preferences"]["output_lang"] == "en"

    tg = data["sources"]["telegram"]
    assert tg["options"] == {"channel": "@news"}      # session_string redacted
    assert "session_string" not in tg["options"]
    assert tg["has_secret"] is True                   # secret presence flagged, value not exposed

    assert len(data["feedback"]) == 1
    assert data["feedback"][0]["topics"] == ["tech"]


def test_delete_removes_everything():
    _setup_user("carol")
    assert accounts._path("carol").exists()
    assert feedback.load("carol")

    summary = privacy.delete_user_data("carol")
    assert summary["removed"]["accounts"] is True
    assert summary["removed"]["feedback_events"] == 1

    # Files gone; a fresh export has defaults and no feedback.
    assert not accounts._path("carol").exists()
    assert feedback.load("carol") == []
    after = privacy.export_user_data("carol")
    assert after["sources"] == {}
    assert after["feedback"] == []


def test_export_unknown_user_has_defaults():
    data = privacy.export_user_data("ghost")
    assert data["user_id"] == "ghost"
    assert data["sources"] == {}
    assert data["feedback"] == []
