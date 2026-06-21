import pytest

from morning_paper import print as printmod
from morning_paper.config import get_settings
from morning_paper.models import PrintAddress
from morning_paper.print.base import get_provider


def test_quote_math_tabloid_us():
    q = get_provider("newspaper_club").quote(format="tabloid", pages=8, copies=3, country="US")
    # unit = 1.20 + 0.07*8 = 1.76 ; subtotal = 5.28 ; printing = max(15, 5.28)=15 ; +14 ship
    assert q.unit_price_usd == pytest.approx(1.76)
    assert q.shipping_usd == pytest.approx(14.0)
    assert q.total_usd == pytest.approx(29.0)
    assert q.estimate is True


def test_quote_uses_subtotal_above_minimum():
    q = get_provider("mixam").quote(format="broadsheet", pages=12, copies=40, country="GB")
    # unit = 1.75 + 0.06*12 = 2.47 ; subtotal = 98.8 (> min 20) ; +8 ship
    assert q.unit_price_usd == pytest.approx(2.47)
    assert q.total_usd == pytest.approx(98.8 + 8.0)


def test_quote_rejects_unsupported_format():
    with pytest.raises(ValueError):
        get_provider("newspaper_club").quote(format="a3", pages=4, copies=1, country="US")


def test_unknown_provider():
    with pytest.raises(KeyError):
        get_provider("nope")


def test_available_providers_lists_formats():
    provs = printmod.available_providers()
    ids = {p["provider_id"] for p in provs}
    assert {"newspaper_club", "mixam"} <= ids
    np = next(p for p in provs if p["provider_id"] == "newspaper_club")
    assert "tabloid" in np["supported_formats"]


def test_count_pdf_pages(tmp_path):
    pdf = tmp_path / "x.pdf"
    pdf.write_bytes(b"%PDF-1.7\n/Type /Pages\n/Type /Page xx /Type/Page yy\n")
    assert printmod.count_pdf_pages(pdf) == 2
    assert printmod.count_pdf_pages(tmp_path / "missing.pdf", default=9) == 9


def test_create_order_needs_credentials_without_key():
    addr = PrintAddress(name="Alex", line1="1 Main St", city="Berlin", country="DE")
    order = printmod.create_order(
        "u", provider_id="newspaper_club", format="broadsheet", copies=2,
        address=addr, pages=8, issue_id="iss1",
    )
    assert order.status == "needs_credentials"
    assert order.provider_order_id is None
    assert order.quote.total_usd > 0
    # persisted + retrievable
    assert printmod.load_order("u", order.id) is not None
    assert [o.id for o in printmod.list_orders("u")] == [order.id]


def test_create_order_submits_with_key(monkeypatch):
    monkeypatch.setenv("NEWSPAPER_CLUB_API_KEY", "secret")
    get_settings.cache_clear()
    addr = PrintAddress(name="Alex", line1="1 Main St", country="US")
    order = printmod.create_order(
        "u2", provider_id="newspaper_club", format="tabloid", copies=1, address=addr, pages=4,
    )
    assert order.status == "submitted"
    assert order.provider_order_id and order.provider_order_id.startswith("newspaper_club-")
    get_settings.cache_clear()
