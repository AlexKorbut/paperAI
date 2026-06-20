import httpx

from morning_paper.retrieval import newsapi


def test_build_query_ors_and_quotes():
    assert newsapi.build_newsapi_query(["AI", "Tour de France"]) == 'AI OR "Tour de France"'


class _FakeResp:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_fetch_maps_articles(monkeypatch):
    payload = {
        "status": "ok",
        "articles": [
            {
                "url": "https://n.com/x",
                "title": "AI milestone",
                "description": "A short description.",
                "publishedAt": "2026-06-19T10:00:00Z",
                "source": {"name": "The Verge"},
            }
        ],
    }
    captured = {}

    def fake_get(url, params=None, headers=None, timeout=None):
        captured["headers"] = headers
        captured["params"] = params
        return _FakeResp(payload)

    monkeypatch.setattr(httpx, "get", fake_get)

    cands = newsapi.fetch_newsapi_candidates(["AI"], api_key="k", language="en")
    assert len(cands) == 1
    c = cands[0]
    assert c.title == "AI milestone"
    assert c.body == "A short description."
    assert c.source == "The Verge"
    assert c.lang == "en"
    assert captured["headers"]["X-Api-Key"] == "k"
    assert captured["params"]["language"] == "en"


def test_fetch_no_key_returns_empty(monkeypatch):
    def boom(*a, **k):  # pragma: no cover
        raise AssertionError("should not hit network without a key")

    monkeypatch.setattr(httpx, "get", boom)
    assert newsapi.fetch_newsapi_candidates(["AI"], api_key="") == []


def test_fetch_api_error_status_returns_empty(monkeypatch):
    monkeypatch.setattr(
        httpx, "get", lambda *a, **k: _FakeResp({"status": "error", "message": "rate limited"})
    )
    assert newsapi.fetch_newsapi_candidates(["AI"], api_key="k") == []
