from __future__ import annotations

import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from morning_paper.api.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_list_issues_returns_list(client: TestClient):
    resp = client.get("/v1/users/demo/issues")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)  # empty until issues are built


def test_cors_allows_cabinet_origin(client: TestClient):
    resp = client.options(
        "/v1/themes",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    # CORS middleware answers the preflight and echoes the allowed origin.
    assert resp.status_code in (200, 204)
    assert resp.headers.get("access-control-allow-origin") == "http://localhost:3000"
