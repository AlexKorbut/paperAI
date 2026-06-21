"""Request/response models for the HTTP API.

These are the public wire contract — deliberately decoupled from internal
dataclasses/ORM rows. Privacy invariants live here: secrets and raw signal text
are never serialized into a response model.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

# Option keys whose values are secret-ish and must never leave the server.
_SECRET_HINTS = ("session", "token", "secret", "password")


def redact_options(options: dict | None) -> dict:
    """Drop secret-ish keys from a source's options dict."""
    if not options:
        return {}
    return {
        k: v
        for k, v in options.items()
        if not any(h in k.lower() for h in _SECRET_HINTS)
    }


# --------------------------------------------------------------------------- #
# Users
# --------------------------------------------------------------------------- #
class UserOut(BaseModel):
    user_id: str
    output_lang: str
    theme: str
    tz: str
    deliver_channel: str


class UserUpdate(BaseModel):
    output_lang: str | None = None
    theme: str | None = None
    tz: str | None = None
    deliver_channel: str | None = None


# --------------------------------------------------------------------------- #
# Sources
# --------------------------------------------------------------------------- #
class SourceInfo(BaseModel):
    source_id: str
    display_name: str
    requires_auth: bool
    config_schema: dict


class SourceAccountOut(BaseModel):
    source_id: str
    enabled: bool
    status: str
    options: dict


class SourceAccountIn(BaseModel):
    enabled: bool = True
    options: dict = Field(default_factory=dict)


# --------------------------------------------------------------------------- #
# Profile
# --------------------------------------------------------------------------- #
class ProfileOut(BaseModel):
    user_id: str
    output_lang: str
    topics: dict[str, float]
    entities: dict[str, float]
    version: int
    updated_at: datetime


# --------------------------------------------------------------------------- #
# Feedback (👍/👎 on stories -> profile learning)
# --------------------------------------------------------------------------- #
class FeedbackIn(BaseModel):
    vote: int = Field(description="+1 for 👍, -1 for 👎")
    issue_id: str | None = None
    story_id: str | None = None
    section: str | None = None
    topics: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)


class FeedbackOut(BaseModel):
    id: str
    user_id: str
    vote: int
    recorded_at: datetime


# --------------------------------------------------------------------------- #
# Themes
# --------------------------------------------------------------------------- #
class ThemeOut(BaseModel):
    id: str
    display_name: str
    mood: str
    page: str
    columns: int
    color_mode: str
    colors: dict
    author: str = ""
    price_usd: float = 0.0


# --------------------------------------------------------------------------- #
# Issues
# --------------------------------------------------------------------------- #
class IssueCreate(BaseModel):
    theme_id: str | None = None
    output_lang: str | None = None
    feed_urls: list[str] = Field(default_factory=list)


class JobOut(BaseModel):
    job_id: str
    issue_id: str | None = None
    status: str


class CostOut(BaseModel):
    cost_usd: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0


class IssueStatusOut(BaseModel):
    issue_id: str
    status: str
    theme_id: str | None = None
    pdf_url: str | None = None
    cost: CostOut = Field(default_factory=CostOut)


class IssueSummary(BaseModel):
    id: str
    theme_id: str | None = None
    status: str
    pdf_url: str | None = None
    created_at: str | None = None


# --------------------------------------------------------------------------- #
# Render (stateless)
# --------------------------------------------------------------------------- #
class RenderRequest(BaseModel):
    """Accept EITHER a full RenderDocument JSON, or fields to build one."""

    document: dict | None = None
    title: str | None = None
    theme_id: str | None = None
    locale: str = "ru"
    stories: list[dict] | None = None
    grid_plan: dict | None = None


class RenderResponse(BaseModel):
    pdf_url: str
    page_count: int | None = None
    warnings: list[str] = Field(default_factory=list)


# --------------------------------------------------------------------------- #
# Print on demand (Phase 3)
# --------------------------------------------------------------------------- #
from ..models import PrintAddress  # noqa: E402  (re-exported for request bodies)


class PrintQuoteRequest(BaseModel):
    provider: str
    format: str
    pages: int = 8
    copies: int = 1
    country: str = "US"


class PrintOrderRequest(BaseModel):
    provider: str
    format: str
    copies: int = 1
    issue_id: str | None = None
    pages: int | None = None
    address: PrintAddress


# --------------------------------------------------------------------------- #
# Groups (Phase 3)
# --------------------------------------------------------------------------- #
class GroupCreate(BaseModel):
    name: str
    owner: str | None = None  # defaults to the calling principal
    members: list[str] = Field(default_factory=list)
    theme: str | None = None
    output_lang: str | None = None


class MemberIn(BaseModel):
    user_id: str


# --------------------------------------------------------------------------- #
# Marketplace (Phase 3)
# --------------------------------------------------------------------------- #
class MarketplaceTheme(BaseModel):
    id: str
    display_name: str
    mood: str = ""
    author: str = ""
    price_usd: float = 0.0
    homepage: str = ""
    license: str = ""
    builtin: bool = True
    third_party: bool = False
