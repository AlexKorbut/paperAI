"""FastAPI application factory.

Routers are mounted under `/v1`. Exception handlers map domain errors to HTTP
status codes so routers can raise/let-propagate plain exceptions.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routers import issues, profile, render, sources, themes, users

# Browser origins allowed to call the API (the Next.js cabinet in dev). Override
# with MP_CORS_ORIGINS="https://app.example.com" (comma-separated) in production.
_DEFAULT_CORS = "http://localhost:3000,http://127.0.0.1:3000"


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    # Best-effort schema creation (SQLite fallback in dev; no-op without a DB layer).
    try:
        from ..db.repository import init_db

        init_db()
    except Exception:
        pass
    yield


def create_app() -> FastAPI:
    # Trigger built-in source registration once at startup.
    import morning_paper.sources  # noqa: F401

    app = FastAPI(title="Morning Paper API", version="v1", lifespan=_lifespan)

    origins = [o.strip() for o in os.environ.get("MP_CORS_ORIGINS", _DEFAULT_CORS).split(",") if o.strip()]
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(users.router, prefix="/v1")
    app.include_router(sources.router, prefix="/v1")
    app.include_router(profile.router, prefix="/v1")
    app.include_router(themes.router, prefix="/v1")
    app.include_router(issues.router, prefix="/v1")
    app.include_router(render.router, prefix="/v1")

    @app.exception_handler(KeyError)
    async def _key_error(_request: Request, exc: KeyError) -> JSONResponse:
        # Unknown source/user/etc. surfaces as KeyError -> 404.
        detail = exc.args[0] if exc.args else "not found"
        return JSONResponse(status_code=404, content={"detail": str(detail)})

    from ..render.renderer import RenderError

    @app.exception_handler(RenderError)
    async def _render_error(_request: Request, exc: RenderError) -> JSONResponse:
        return JSONResponse(status_code=502, content={"detail": str(exc)})

    return app


# Module-level app for `uvicorn morning_paper.api.app:app`.
app = create_app()
