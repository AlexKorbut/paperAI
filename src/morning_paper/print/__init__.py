"""Print-on-demand (Phase 3): turn a rendered issue into a real newspaper.

Providers (Newspaper Club, Mixam) are abstracted behind ``PrintProvider`` so the
rest of the system asks for a quote or places an order without knowing the
vendor. Pricing is a transparent heuristic until a real provider account/API key
is configured; submission records the order and marks it ``needs_credentials``
when no key is present, rather than pretending it shipped.
"""

from .base import PrintProvider, PROVIDERS, get_provider, list_providers
from .service import (
    available_providers,
    count_pdf_pages,
    create_order,
    list_orders,
    load_order,
    quote,
)

__all__ = [
    "PrintProvider",
    "PROVIDERS",
    "get_provider",
    "list_providers",
    "available_providers",
    "quote",
    "create_order",
    "list_orders",
    "load_order",
    "count_pdf_pages",
]
