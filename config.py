from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Settings(BaseSettings):
    openai_api_key: str
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    provider: Literal["openai", "anthropic", "google"] = "openai"

    gpt_version: str = "gpt-5-2025-08-07"
    claude_version: str = "claude-3-7-sonnet-20250219"
    gemini_version: str = "gemini-2.0-flash"
    env: str ="dev"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def get_current_model(self) -> str:
        if self.provider == "openai":
            return self.gpt_version
        elif self.provider == "anthropic":
            return self.claude_version
        elif self.provider == "google":
            return self.gemini_version

@lru_cache
def get_settings():
    return Settings()