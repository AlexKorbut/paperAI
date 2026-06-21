"""Core data contracts shared across the whole pipeline.

These types are the seams between subsystems. The interest-source plugins emit
`Signal`s; the profile builder produces an `InterestProfile`; retrieval yields
`Candidate`s that become `Story`s; the editorial stage produces a `GridPlan`;
and the only thing crossing the Python<->Node renderer boundary is a fully
semantic `RenderDocument` (no fonts, colors, or pixels — those live in themes).
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------- #
# Interest signals (Subsystem 1: pluggable sources)
# --------------------------------------------------------------------------- #
class SignalKind(str, Enum):
    """What a signal represents, ordered roughly by how strongly it implies interest."""

    SUBSCRIPTION = "subscription"  # follows a channel/account (mid)
    MESSAGE = "message"            # text from a personal/group chat (mid, private)
    READ = "read"                  # opened/read something (mid)
    SURVEY = "survey"              # picked a topic in onboarding (high)
    SAVE = "save"                  # saved/bookmarked a post (high)
    REACTION = "reaction"          # reacted/liked (high)
    FORWARD = "forward"            # forwarded/shared (high)
    FREE_TEXT = "free_text"        # typed their interests in prose (high)
    FEEDBACK = "feedback"          # in-product 👍/👎 on a story (high, dynamic)


# Default prior weight per kind (see docs/03-interest-parsing.md signal-strength table).
DEFAULT_STRENGTH: dict[SignalKind, float] = {
    SignalKind.SUBSCRIPTION: 0.5,
    SignalKind.MESSAGE: 0.5,
    SignalKind.READ: 0.5,
    SignalKind.SURVEY: 0.8,
    SignalKind.SAVE: 0.85,
    SignalKind.REACTION: 0.85,
    SignalKind.FORWARD: 0.9,
    SignalKind.FREE_TEXT: 0.9,
    SignalKind.FEEDBACK: 0.9,
}


class Signal(BaseModel):
    """A normalized unit of evidence about what a user is interested in.

    Every interest source emits these and nothing else, so the profile builder
    is agnostic to where a signal came from.
    """

    id: str
    user_id: str
    source_id: str
    kind: SignalKind
    text: str
    lang: str | None = None
    strength: float = Field(default=0.5, ge=0.0, le=1.0)
    entities_hint: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_private: bool = False
    raw_ref: str | None = None  # object-store key if raw kept; None if discarded (privacy)

    @classmethod
    def make(
        cls,
        *,
        user_id: str,
        source_id: str,
        kind: SignalKind,
        text: str,
        external_id: str | None = None,
        strength: float | None = None,
        **kw,
    ) -> "Signal":
        """Construct a Signal with a stable id and a kind-appropriate default strength."""
        basis = external_id or text
        sig_id = hashlib.sha256(f"{source_id}:{basis}".encode()).hexdigest()[:24]
        return cls(
            id=sig_id,
            user_id=user_id,
            source_id=source_id,
            kind=kind,
            text=text,
            strength=DEFAULT_STRENGTH[kind] if strength is None else strength,
            **kw,
        )


# --------------------------------------------------------------------------- #
# Interest profile (3 layers: topics, entities, semantic vectors)
# --------------------------------------------------------------------------- #
class InterestProfile(BaseModel):
    user_id: str
    output_lang: str = "ru"
    topics: dict[str, float] = Field(default_factory=dict)        # taxonomy path -> weight
    entities: dict[str, float] = Field(default_factory=dict)      # normalized entity -> weight
    interest_vectors: list[list[float]] = Field(default_factory=list)  # cluster centroids
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 1


class Feedback(BaseModel):
    """In-product 👍/👎 on a rendered story, folded back into the profile.

    The vote carries the topics/entities the story was about so it can nudge the
    matching profile weights up (👍 = +1) or down (👎 = -1). It never stores
    article text — only the labels — keeping the privacy invariant intact.
    """

    id: str
    user_id: str
    vote: Literal[1, -1]
    issue_id: str | None = None
    story_id: str | None = None
    section: str | None = None
    topics: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def make(
        cls,
        *,
        user_id: str,
        vote: int,
        issue_id: str | None = None,
        story_id: str | None = None,
        section: str | None = None,
        topics: list[str] | None = None,
        entities: list[str] | None = None,
        **kw,
    ) -> "Feedback":
        ts = datetime.now(timezone.utc)
        basis = f"{user_id}:{issue_id}:{story_id}:{vote}:{ts.timestamp()}"
        fid = hashlib.sha256(basis.encode()).hexdigest()[:24]
        return cls(
            id=fid,
            user_id=user_id,
            vote=1 if vote >= 0 else -1,
            issue_id=issue_id,
            story_id=story_id,
            section=section,
            topics=list(topics or []),
            entities=list(entities or []),
            created_at=ts,
            **kw,
        )


# --------------------------------------------------------------------------- #
# Print-on-demand (Phase 3)
# --------------------------------------------------------------------------- #
class PrintAddress(BaseModel):
    name: str
    line1: str
    line2: str = ""
    city: str = ""
    postcode: str = ""
    country: str = "US"  # ISO-3166 alpha-2; drives shipping estimate


class PrintQuote(BaseModel):
    provider: str
    format: str
    pages: int
    copies: int
    unit_price_usd: float
    shipping_usd: float
    total_usd: float
    currency: str = "USD"
    estimate: bool = True  # heuristic until a real provider account is wired


class PrintOrder(BaseModel):
    id: str
    user_id: str
    provider: str
    format: str
    pages: int
    copies: int
    address: PrintAddress
    quote: PrintQuote
    issue_id: str | None = None
    # draft | quoted | submitted | needs_credentials | failed
    status: str = "draft"
    provider_order_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def make(cls, *, user_id: str, provider: str, quote: "PrintQuote",
             address: "PrintAddress", copies: int, issue_id: str | None = None, **kw) -> "PrintOrder":
        ts = datetime.now(timezone.utc)
        oid = hashlib.sha256(
            f"{user_id}:{provider}:{issue_id}:{ts.timestamp()}".encode()
        ).hexdigest()[:20]
        return cls(
            id=oid, user_id=user_id, provider=provider, format=quote.format,
            pages=quote.pages, copies=copies, address=address, quote=quote,
            issue_id=issue_id, created_at=ts, **kw,
        )


# --------------------------------------------------------------------------- #
# Family / team groups (Phase 3): one shared paper for several people
# --------------------------------------------------------------------------- #
class Group(BaseModel):
    id: str
    name: str
    owner: str
    members: list[str] = Field(default_factory=list)
    theme: str | None = None
    output_lang: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def make(cls, *, name: str, owner: str, members: list[str] | None = None,
             theme: str | None = None, output_lang: str | None = None) -> "Group":
        gid = hashlib.sha256(f"{owner}:{name}".encode()).hexdigest()[:16]
        mem = list(dict.fromkeys([owner, *(members or [])]))  # owner always a member, de-duped
        return cls(id=gid, name=name, owner=owner, members=mem, theme=theme, output_lang=output_lang)


# --------------------------------------------------------------------------- #
# Candidates and stories (retrieval -> editorial)
# --------------------------------------------------------------------------- #
class Candidate(BaseModel):
    """A news article fetched by retrieval, before editorial processing."""

    id: str
    title: str
    url: str
    source: str
    lang: str | None = None
    published_at: datetime | None = None
    summary_src: str | None = None      # original-language snippet/body
    image_url: str | None = None
    score: float = 0.0                  # relevance to the profile (filled by rank)


class Story(BaseModel):
    """A candidate after summarize+translate — ready to be placed on the page."""

    id: str
    section: str
    headline: str
    deck: str | None = None             # subhead / standfirst
    body_html: str                      # newspaper-register prose, in output_lang
    byline: str | None = None
    source: str
    source_url: str
    image_ref: str | None = None        # object-store key
    pull_quote: str | None = None


# --------------------------------------------------------------------------- #
# Editorial grid plan (Opus decision, validated before rendering)
# --------------------------------------------------------------------------- #
StorySize = Literal["lead", "medium", "brief"]


class GridSlot(BaseModel):
    story_id: str
    section: str
    size: StorySize
    columns: int = Field(ge=1)
    with_photo: bool = False
    pull_quote: str | None = None


class GridPlan(BaseModel):
    page_format: str = "a4"
    section_order: list[str] = Field(default_factory=list)
    slots: list[GridSlot] = Field(default_factory=list)

    def validate_against_theme(self, *, columns: int, max_lead: int) -> list[str]:
        """Return a list of constraint violations (empty == valid)."""
        problems: list[str] = []
        leads = [s for s in self.slots if s.size == "lead"]
        if len(leads) > max_lead:
            problems.append(f"{len(leads)} lead slots, theme allows {max_lead}")
        for s in self.slots:
            if s.columns > columns:
                problems.append(f"slot {s.story_id} spans {s.columns} > {columns} columns")
        return problems


# --------------------------------------------------------------------------- #
# Render document (the single JSON contract crossing into the Node renderer)
# --------------------------------------------------------------------------- #
RENDER_SCHEMA_VERSION = 1


class StoryView(BaseModel):
    """Theme-agnostic view of a story for the renderer."""

    headline: str
    deck: str | None = None
    body_html: str
    byline: str | None = None
    caption: str | None = None
    image_ref: str | None = None


class Masthead(BaseModel):
    title: str
    date: str
    issue_no: str | None = None
    edition: str | None = None


class RenderDocument(BaseModel):
    schema_version: int = RENDER_SCHEMA_VERSION
    issue_id: str
    theme_id: str
    locale: str = "ru"
    masthead: Masthead
    grid_plan: GridPlan
    stories: dict[str, StoryView]
    images: dict[str, str] = Field(default_factory=dict)  # image_ref -> object key/path
