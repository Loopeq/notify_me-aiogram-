import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = os.environ["BOT_TOKEN"]


settings = Settings(_case_sensitive=False)

