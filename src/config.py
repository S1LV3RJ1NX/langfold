import os
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Settings class to hold all the environment variables
    """

    # Log level can be configured via environment variable, defaults to INFO
    LOG_LEVEL: str = "INFO"
    LITELLM_GATEWAY_URL: str
    LITELLM_GATEWAY_API_KEY: str

    AGENT_CONFIG: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "agent.yaml"
    )

    # Check if the agent config path exists, if not raise an error, else load the yaml file
    @field_validator("AGENT_CONFIG")
    @classmethod
    def check_agent_config_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Agent config path {v} does not exist.")
        return v

    # Load the yaml file
    @field_validator("AGENT_CONFIG")
    @classmethod
    def load_agent_config(cls, v):
        with open(v, "r") as f:
            return yaml.safe_load(f)

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


settings = Settings()
