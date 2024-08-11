import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import logging

DEV_MODE = True


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger().setLevel(logging.INFO)


if DEV_MODE:
    load_dotenv(dotenv_path='.env')
    logger.info(f"{DEV_MODE=}")


class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv('BOT_TOKEN') if DEV_MODE else os.environ["BOT_TOKEN"]


settings = Settings(_case_sensitive=False)

