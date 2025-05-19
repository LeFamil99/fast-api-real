import os
import sys
from functools import cache
from loguru import logger

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV =  "dev"
CONFIG_YAML_DIR = os.path.normpath(f"configs/{ENV}.config.yaml")
# CONFIG_YAML_DIR = f"configs/{ENV}.config.yaml"


class Config(BaseSettings):
    api_key: str = "1234567890"
    debug: bool = False
    model_config = SettingsConfigDict(yaml_file=CONFIG_YAML_DIR, extra="ignore")

@cache
def get_config() -> Config:
    app_config = Config()

    # TODO
    logging_level = "DEBUG" if app_config.debug else "INFO"
    logger.remove(0)
    logger.add(sys.stdout, level=logging_level)

    return app_config
