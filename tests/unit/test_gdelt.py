import httpx
import pytest

from morning_paper.retrieval import gdelt


def test_build_query_single_term_no_parens():
    assert gdelt.build_gdelt_query(["Anthropic"]) == "Anthropic"


def test_build_query_ors_and_quotes_phrases():
    q = gdelt.build_gdelt_query(["Anthropic", "Tour de France"])
    assert q == '(Anthropic OR "Tour de France")'


def test_build_query_with_language_filter():
    q = gdelt.build_gdelt_query(["AI"], source_langs=["English", "Russian"])
    assert q == "AI (sourcelang:English OR sourcelang:Russian)"


def test_build_query_empty():
    assert gdelt.build_gdelt_query([]) == ""


class _FakeResp:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_fetch_maps_articles(monkeypatch):
    payload = {
        "articles": [
            {
                "url": "https://ex.com/a",
                "title": "Заголовок про ИИ",
                "seendate": "20260619T120000Z",
                "domain": "ex.com",
                "language": "Russian",
            },
            {  # missing title -> skipped
                "url": "https://ex.com/b",
                "title": "",
                "seendate": "",
            },
        ]
    }
    captured = {}

    def fake_get(url, params=None, timeout=None):
        captured["url"] = url
        captured["params"] = params
        return _FakeResp(payload)

    monkeypatch.setattr(httpx, "get", fake_get)

    cands = gdelt.fetch_gdelt_candidates(["ИИ"], max_records=10, timespan="1d")
    assert len(cands) == 1
    c = cands[0]
    assert c.title == "Заголовок про ИИ"
    assert c.lang == "Russian"
    assert c.source == "ex.com"
    assert c.url == "https://ex.com/a"
    assert c.published_at.startswith("2026-06-19T12:00:00")
    # query params wired through
    assert captured["params"]["mode"] == "ArtList"
    assert captured["params"]["maxrecords"] == "10"


def test_fetch_network_error_returns_empty(monkeypatch):
    def boom(*a, **k):
        raise httpx.ConnectError("no network")

    monkeypatch.setattr(httpx, "get", boom)
    assert gdelt.fetch_gdelt_candidates(["AI"]) == []


def test_fetch_no_terms_short_circuits(monkeypatch):
    def boom(*a, **k):  # pragma: no cover - must not be called
        raise AssertionError("should not hit network with no terms")

    monkeypatch.setattr(httpx, "get", boom)
    assert gdelt.fetch_gdelt_candidates([]) == []
