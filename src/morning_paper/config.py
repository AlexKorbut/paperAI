"""Typed settings: non-secret config from config/settings.toml, secrets from env."""

from __future__ import annotations

import tomllib
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # morning-paper/
CONFIG_DIR = PROJECT_ROOT / "config"
THEMES_DIR = PROJECT_ROOT / "themes"
RENDERER_DIR = PROJECT_ROOT / "renderer"


class Defaults(BaseModel):
    output_lang: str = "ru"
    theme: str = "times-classic"
    page_format: str = "a4"


class ModelRouting(BaseModel):
    tagging: str = "claude-haiku-4-5"
    summarize: str = "claude-sonnet-4-6"
    editorial: str = "claude-opus-4-8"


class LLMOptions(BaseModel):
    use_batch: bool = True
    use_prompt_cache: bool = True


class EmbeddingsConfig(BaseModel):
    provider: str = "voyage"
    model: str = "voyage-3.5"          # multilingual embedding model
    semantic_weight: float = 0.6       # blend: semantic vs keyword in ranking (0..1)


class RetrievalConfig(BaseModel):
    max_candidates: int = 300
    final_stories: int = 30
    gdelt_enabled: bool = True
    gdelt_timespan: str = "1d"         # GDELT lookback window (e.g. 1d, 12h)
    gdelt_max_records: int = 75
    source_langs: list[str] = []       # empty = accept every source language


class FileConfig(BaseModel):
    """The parsed contents of settings.toml."""

    defaults: Defaults = Defaults()
    models: ModelRouting = ModelRouting()
    llm: LLMOptions = LLMOptions()
    embeddings: EmbeddingsConfig = EmbeddingsConfig()
    retrieval: RetrievalConfig = RetrievalConfig()


class Secrets(BaseSettings):
    """Secrets and connection strings, pulled from the environment / .env."""

    model_config = SettingsConfigDict(env_prefix="", env_file=".env", extra="ignore")

    anthropic_api_key: str | None = None
    voyage_api_key: str | None = None
    mp_db_url: str | None = None
    mp_object_store_url: str = "file://./.data/objects"
    mp_broker_url: str | None = None        # Celery broker (e.g. redis://localhost:6379/0)
    mp_result_backend: str | None = None    # Celery result backend (defaults to broker)
    telegram_api_id: str | None = None   # used by the Telethon connector (TELEGRAM_API_ID)
    telegram_api_hash: str | None = None
    newsapi_key: str | None = None
    telegram_bot_token: str | None = None
    resend_api_key: str | None = None
    newspaper_club_api_key: str | None = None  # print-on-demand (Phase 3)
    mixam_api_key: str | None = None


class Settings(BaseModel):
    file: FileConfig
    secrets: Secrets


def _load_file_config() -> FileConfig:
    path = CONFIG_DIR / "settings.toml"
    if not path.exists():
        return FileConfig()
    with path.open("rb") as fh:
        return FileConfig.model_validate(tomllib.load(fh))


@lru_cache
def get_settings() -> Settings:
    return Settings(file=_load_file_config(), secrets=Secrets())
