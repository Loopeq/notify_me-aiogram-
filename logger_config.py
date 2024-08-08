from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time} {level} {message}")
logger.add("debug.log", format="{time} {level} {message}",
           level="INFO", rotation="500 MB")
