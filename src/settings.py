from pydantic_settings import BaseSettings
from pathlib import Path

CURRENT_PATH = Path(__file__).resolve()
ROOT = CURRENT_PATH.parent.parent
ENV_ROOT = ROOT / ".env"


class Settings(BaseSettings):
    BOT_TOKEN: str

    class Config:
        env_file = ENV_ROOT


settings = Settings(_case_sensitive=False)

