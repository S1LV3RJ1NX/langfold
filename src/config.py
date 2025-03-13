import os
import yaml
from typing import Dict
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


PRIMARY_CONFIG = "primary"


class Settings(BaseSettings):
    """
    Settings class to hold all the environment variables and agent configurations
    """

    # Log level can be configured via environment variable, defaults to INFO
    LOG_LEVEL: str = "INFO"
    LITELLM_GATEWAY_URL: str
    LITELLM_GATEWAY_API_KEY: str

    # Directory containing all agent configurations
    CONFIG_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "configs/agents"
    )

    # Primary agent config file that must exist
    PRIMARY_CONFIG: str = PRIMARY_CONFIG

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


settings = Settings()
