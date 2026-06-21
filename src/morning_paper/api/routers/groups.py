"""Family / team groups: shared paper for several members."""

from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from ...models import Group
from ..deps import Principal, get_principal, require_owner
from ..schemas import GroupCreate, JobOut, MemberIn

router = APIRouter(tags=["groups"])


@router.post("/groups", response_model=Group, status_code=201)
def create_group(body: GroupCreate, principal: Principal = Depends(get_principal)) -> Group:
    from ... import groups

    owner = body.owner or principal.subject
    require_owner(principal, owner)
    return groups.create(
        body.name, owner, members=body.members, theme=body.theme, output_lang=body.output_lang
    )


@router.get("/groups", response_model=list[Group])
def list_groups(principal: Principal = Depends(get_principal)) -> list[Group]:
    from ... import groups

    return groups.list_groups(owner=principal.subject)


@router.get("/groups/{group_id}", response_model=Group)
def get_group(group_id: str, principal: Principal = Depends(get_principal)) -> Group:
    from ... import groups

    g = groups.load(group_id)
    if g is None:
        raise HTTPException(404, f"no group {group_id!r}")
    return g


@router.post("/groups/{group_id}/members", response_model=Group)
def add_member(group_id: str, body: MemberIn, principal: Principal = Depends(get_principal)) -> Group:
    from ... import groups

    try:
        return groups.add_member(group_id, body.user_id)
    except KeyError as e:
        raise HTTPException(404, str(e))


@router.delete("/groups/{group_id}/members/{user_id}", response_model=Group)
def remove_member(group_id: str, user_id: str, principal: Principal = Depends(get_principal)) -> Group:
    from ... import groups

    try:
        return groups.remove_member(group_id, user_id)
    except KeyError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(422, str(e))


@router.delete("/groups/{group_id}")
def delete_group(group_id: str, principal: Principal = Depends(get_principal)) -> dict:
    from ... import groups

    return {"deleted": groups.delete(group_id)}


@router.post("/groups/{group_id}/issues", response_model=JobOut, status_code=202)
def create_group_issue(
    group_id: str, background: BackgroundTasks, principal: Principal = Depends(get_principal)
) -> JobOut:
    """Build one shared issue for the group, in the background."""
    from ... import groups

    if groups.load(group_id) is None:
        raise HTTPException(404, f"no group {group_id!r}")
    # Group issue runs the pipeline once + multi-delivery; do it off the request.
    background.add_task(groups.run_group_issue, group_id)
    return JobOut(job_id=group_id, issue_id=None, status="queued")
