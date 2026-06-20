"""Interest profile: build (ingest+tag) and read.

Never returns raw signal text — only topic/entity weights.
"""

from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from ..deps import Principal, get_principal, require_owner
from ..jobs import submit_issue
from ..schemas import FeedbackIn, FeedbackOut, JobOut, ProfileOut

router = APIRouter(tags=["profile"])


@router.post("/users/{user_id}/profile:build", response_model=JobOut)
def build_profile(
    user_id: str,
    background: BackgroundTasks,
    principal: Principal = Depends(get_principal),
) -> JobOut:
    # Build the profile by running ingest+tag stages only (1..2). The pipeline
    # persists the profile internally, so we reuse the same async job path.
    require_owner(principal, user_id)
    result = submit_issue(user_id, {"until_stage": 2}, background=background)
    return JobOut(job_id=result["issue_id"], issue_id=result["issue_id"], status=result["status"])


@router.get("/users/{user_id}/profile", response_model=ProfileOut)
def get_profile(
    user_id: str, principal: Principal = Depends(get_principal)
) -> ProfileOut:
    require_owner(principal, user_id)
    from ...db.repository import load_profile

    profile = load_profile(user_id)
    if profile is None:
        raise HTTPException(404, f"no profile for user {user_id!r}")
    return ProfileOut(
        user_id=profile.user_id,
        output_lang=profile.output_lang,
        topics=dict(profile.topics),
        entities=dict(profile.entities),
        version=profile.version,
        updated_at=profile.updated_at,
    )


@router.post("/users/{user_id}/feedback", response_model=FeedbackOut, status_code=201)
def post_feedback(
    user_id: str, body: FeedbackIn, principal: Principal = Depends(get_principal)
) -> FeedbackOut:
    """Record 👍/👎 on a story. Folded into the profile on the next build."""
    require_owner(principal, user_id)
    if body.vote not in (1, -1):
        raise HTTPException(422, "vote must be +1 or -1")

    from ... import feedback as fb
    from ...models import Feedback

    event = Feedback.make(
        user_id=user_id,
        vote=body.vote,
        issue_id=body.issue_id,
        story_id=body.story_id,
        section=body.section,
        topics=body.topics,
        entities=body.entities,
    )
    fb.record(event)
    return FeedbackOut(
        id=event.id, user_id=user_id, vote=event.vote, recorded_at=event.created_at
    )
