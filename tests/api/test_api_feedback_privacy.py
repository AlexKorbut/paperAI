from __future__ import annotations

import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from morning_paper.api.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_feedback_post_records(client: TestClient):
    resp = client.post(
        "/v1/users/demo/feedback",
        json={"vote": 1, "story_id": "s-ai", "topics": ["tech"], "entities": ["Anthropic"]},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["vote"] == 1 and body["user_id"] == "demo" and body["id"]


def test_feedback_rejects_bad_vote(client: TestClient):
    resp = client.post("/v1/users/demo/feedback", json={"vote": 0})
    assert resp.status_code == 422


def test_export_and_delete_data(client: TestClient):
    # Seed a preference + a feedback event.
    client.put("/v1/users/demo", json={"theme": "economist"})
    client.post("/v1/users/demo/feedback", json={"vote": -1, "topics": ["sport"]})

    exported = client.get("/v1/users/demo/data:export")
    assert exported.status_code == 200
    data = exported.json()
    assert data["preferences"]["theme"] == "economist"
    assert len(data["feedback"]) == 1

    deleted = client.request("DELETE", "/v1/users/demo/data")
    assert deleted.status_code == 200
    assert deleted.json()["removed"]["feedback_events"] == 1

    after = client.get("/v1/users/demo/data:export").json()
    assert after["feedback"] == []
