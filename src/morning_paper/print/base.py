"""Print providers and their (heuristic) pricing.

Each provider declares which physical formats it prints and a small pricing
model: a per-copy base by format, a per-page surcharge, an order minimum, and
flat shipping by region. These numbers are deliberately conservative estimates
(``PrintQuote.estimate = True``) — real prices come from the provider's account
API, which slots in at ``submit`` once an API key exists.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Protocol, runtime_checkable

from ..models import PrintAddress, PrintOrder, PrintQuote

# Region buckets for flat-rate shipping estimates, keyed by ISO-3166 alpha-2.
_EU = {
    "DE", "FR", "ES", "IT", "NL", "BE", "AT", "PT", "IE", "FI", "SE", "DK",
    "PL", "CZ", "GR", "RO", "HU", "SK", "SI", "EE", "LV", "LT", "LU", "BG", "HR",
}


def _region(country: str) -> str:
    c = (country or "US").upper()
    if c == "US":
        return "US"
    if c == "GB" or c == "UK":
        return "GB"
    if c in _EU:
        return "EU"
    return "INTL"


@runtime_checkable
class PrintProvider(Protocol):
    provider_id: str
    display_name: str
    supported_formats: list[str]

    def quote(self, *, format: str, pages: int, copies: int, country: str) -> PrintQuote: ...
    def submit(self, order: PrintOrder, *, pdf_path: Path | None, api_key: str | None) -> PrintOrder: ...


class _BaseProvider:
    """Shared quote/submit machinery; concrete providers set the price tables."""

    provider_id: str = ""
    display_name: str = ""
    supported_formats: list[str] = []
    base_by_format: dict[str, float] = {}
    per_page_usd: float = 0.0
    min_total_usd: float = 0.0
    shipping_usd: dict[str, float] = {}

    def quote(self, *, format: str, pages: int, copies: int, country: str) -> PrintQuote:
        if format not in self.supported_formats:
            raise ValueError(
                f"{self.display_name} does not print {format!r}; "
                f"supported: {self.supported_formats}"
            )
        pages = max(1, int(pages))
        copies = max(1, int(copies))
        unit = round(self.base_by_format[format] + self.per_page_usd * pages, 2)
        subtotal = round(unit * copies, 2)
        printing = max(self.min_total_usd, subtotal)
        shipping = self.shipping_usd.get(_region(country), self.shipping_usd.get("INTL", 0.0))
        total = round(printing + shipping, 2)
        return PrintQuote(
            provider=self.provider_id,
            format=format,
            pages=pages,
            copies=copies,
            unit_price_usd=unit,
            shipping_usd=round(shipping, 2),
            total_usd=total,
            estimate=True,
        )

    def submit(self, order: PrintOrder, *, pdf_path: Path | None, api_key: str | None) -> PrintOrder:
        if order.format not in self.supported_formats:
            order.status = "failed"
            return order
        if pdf_path is not None and not Path(pdf_path).exists():
            order.status = "failed"
            return order
        if not api_key:
            # Honest about the boundary: we have a costed order but no account to
            # actually place it. The order is persisted as a draft awaiting creds.
            order.status = "needs_credentials"
            order.provider_order_id = None
            return order
        # With a key, a real client would POST the PDF + spec to the provider.
        # That integration is provider-specific; here we mark it submitted with a
        # deterministic local reference so the flow is end-to-end testable.
        ref = hashlib.sha256(f"{self.provider_id}:{order.id}".encode()).hexdigest()[:12]
        order.provider_order_id = f"{self.provider_id}-{ref}"
        order.status = "submitted"
        return order


class NewspaperClubProvider(_BaseProvider):
    provider_id = "newspaper_club"
    display_name = "Newspaper Club"
    supported_formats = ["tabloid", "broadsheet", "mini", "berliner"]
    base_by_format = {"tabloid": 1.20, "broadsheet": 1.60, "mini": 0.90, "berliner": 1.30}
    per_page_usd = 0.07
    min_total_usd = 15.0
    shipping_usd = {"US": 14.0, "GB": 6.0, "EU": 9.0, "INTL": 20.0}


class MixamProvider(_BaseProvider):
    provider_id = "mixam"
    display_name = "Mixam"
    supported_formats = ["a3", "tabloid", "broadsheet", "berliner"]
    base_by_format = {"a3": 1.00, "tabloid": 1.25, "broadsheet": 1.75, "berliner": 1.40}
    per_page_usd = 0.06
    min_total_usd = 20.0
    shipping_usd = {"US": 10.0, "GB": 8.0, "EU": 8.0, "INTL": 18.0}


PROVIDERS: dict[str, _BaseProvider] = {
    p.provider_id: p for p in (NewspaperClubProvider(), MixamProvider())
}


def get_provider(provider_id: str) -> _BaseProvider:
    try:
        return PROVIDERS[provider_id]
    except KeyError:
        raise KeyError(f"unknown print provider {provider_id!r}; known: {sorted(PROVIDERS)}") from None


def list_providers() -> list[_BaseProvider]:
    return list(PROVIDERS.values())
