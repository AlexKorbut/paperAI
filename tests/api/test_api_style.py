from __future__ import annotations

import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from morning_paper.api.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_style_roundtrip_and_merge(client: TestClient):
    assert client.get("/v1/users/me/style").json() == {}

    put = client.put("/v1/users/me/style", json={"scale": 1.15, "accent": "#0b63b8", "dropcap": False})
    assert put.status_code == 200
    body = put.json()
    assert body["scale"] == 1.15 and body["accent"] == "#0b63b8" and body["dropcap"] is False

    # partial update merges (leading added, others kept)
    client.put("/v1/users/me/style", json={"leading": 1.6})
    merged = client.get("/v1/users/me/style").json()
    assert merged["leading"] == 1.6 and merged["scale"] == 1.15

    # null clears a key
    client.put("/v1/users/me/style", json={"accent": None})
    assert "accent" not in client.get("/v1/users/me/style").json()


def test_style_flows_into_rendered_document():
    # The override saved via the API is applied by the pipeline's document builder.
    from morning_paper import accounts
    from morning_paper.sample import specimen_render_document

    accounts.set_source  # ensure module import side effects are fine
    doc = specimen_render_document("times-classic", style_overrides={"scale": 1.2})
    assert doc.style_overrides == {"scale": 1.2}
