"""Print-on-demand: providers, quotes, and per-user orders."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ...models import PrintOrder, PrintQuote
from ..deps import Principal, get_principal, get_store, require_owner
from ..schemas import PrintOrderRequest, PrintQuoteRequest

router = APIRouter(tags=["print"])


@router.get("/print/providers")
def providers() -> list[dict]:
    from ... import print as printmod

    return printmod.available_providers()


@router.post("/print/quote", response_model=PrintQuote)
def quote(req: PrintQuoteRequest) -> PrintQuote:
    from ... import print as printmod

    try:
        return printmod.quote(
            req.provider, format=req.format, pages=req.pages, copies=req.copies, country=req.country
        )
    except KeyError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(422, str(e))


@router.post("/users/{user_id}/print-orders", response_model=PrintOrder, status_code=201)
def create_order(
    user_id: str, req: PrintOrderRequest, principal: Principal = Depends(get_principal)
) -> PrintOrder:
    require_owner(principal, user_id)
    from ... import print as printmod

    pdf_path = None
    if req.issue_id:
        try:
            pdf_path = get_store().open_path(f"issues/{req.issue_id}/issue.pdf")
        except Exception:
            pdf_path = None
    try:
        return printmod.create_order(
            user_id,
            provider_id=req.provider,
            format=req.format,
            copies=req.copies,
            address=req.address,
            issue_id=req.issue_id,
            pages=req.pages,
            pdf_path=pdf_path,
        )
    except KeyError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(422, str(e))


@router.get("/users/{user_id}/print-orders", response_model=list[PrintOrder])
def list_orders(user_id: str, principal: Principal = Depends(get_principal)) -> list[PrintOrder]:
    require_owner(principal, user_id)
    from ... import print as printmod

    return printmod.list_orders(user_id)


@router.get("/users/{user_id}/print-orders/{order_id}", response_model=PrintOrder)
def get_order(
    user_id: str, order_id: str, principal: Principal = Depends(get_principal)
) -> PrintOrder:
    require_owner(principal, user_id)
    from ... import print as printmod

    order = printmod.load_order(user_id, order_id)
    if order is None:
        raise HTTPException(404, f"no order {order_id!r}")
    return order
