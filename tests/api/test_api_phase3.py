from __future__ import annotations

import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from morning_paper.api.app import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


# ---- Print -------------------------------------------------------------- #
def test_print_providers_and_quote(client: TestClient):
    provs = client.get("/v1/print/providers").json()
    assert any(p["provider_id"] == "newspaper_club" for p in provs)

    q = client.post(
        "/v1/print/quote",
        json={"provider": "mixam", "format": "a3", "pages": 8, "copies": 2, "country": "US"},
    )
    assert q.status_code == 200
    assert q.json()["total_usd"] > 0


def test_print_quote_unsupported_format(client: TestClient):
    r = client.post("/v1/print/quote", json={"provider": "newspaper_club", "format": "a3"})
    assert r.status_code == 422


def test_print_order_roundtrip(client: TestClient):
    body = {
        "provider": "newspaper_club",
        "format": "tabloid",
        "copies": 2,
        "pages": 8,
        "address": {"name": "Alex", "line1": "1 Main", "country": "US"},
    }
    created = client.post("/v1/users/me/print-orders", json=body)
    assert created.status_code == 201
    order = created.json()
    assert order["status"] == "needs_credentials"  # no provider key in tests
    assert order["quote"]["total_usd"] > 0

    listed = client.get("/v1/users/me/print-orders").json()
    assert [o["id"] for o in listed] == [order["id"]]
    got = client.get(f"/v1/users/me/print-orders/{order['id']}")
    assert got.status_code == 200 and got.json()["id"] == order["id"]


# ---- Groups ------------------------------------------------------------- #
def test_group_lifecycle(client: TestClient):
    created = client.post(
        "/v1/groups",
        json={"name": "Family", "members": ["partner"], "theme": "economist"},
    )
    assert created.status_code == 201
    g = created.json()
    assert g["owner"] == "me"  # defaults to principal
    assert set(g["members"]) == {"me", "partner"}

    gid = g["id"]
    assert any(x["id"] == gid for x in client.get("/v1/groups").json())

    added = client.post(f"/v1/groups/{gid}/members", json={"user_id": "kid"}).json()
    assert "kid" in added["members"]

    removed = client.request("DELETE", f"/v1/groups/{gid}/members/kid").json()
    assert "kid" not in removed["members"]

    # cannot remove owner
    assert client.request("DELETE", f"/v1/groups/{gid}/members/me").status_code == 422


# ---- Marketplace + themes metadata -------------------------------------- #
def test_marketplace_lists_builtins(client: TestClient):
    items = {i["id"]: i for i in client.get("/v1/marketplace/themes").json()}
    assert items["economist"]["builtin"] is True


def test_themes_endpoint_has_marketplace_fields(client: TestClient):
    themes = client.get("/v1/themes").json()
    assert all("author" in t and "price_usd" in t for t in themes)
