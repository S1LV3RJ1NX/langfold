import os
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Settings class to hold all the environment variables
    """

    LOG_LEVEL: str = "INFO"

    LITELLM_GATEWAY_URL: str = ""
    LITELLM_GATEWAY_API_KEY: str = ""

    TFY_GATEWAY_URL: str = ""
    TFY_GATEWAY_API_KEY: str = ""

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

    # Either one of the gateway is required
    @field_validator("LITELLM_GATEWAY_URL", "TFY_GATEWAY_URL")
    @classmethod
    def check_gateway_url(cls, v, info):
        values = info.data
        if (
            not v
            and not values.get("TFY_GATEWAY_URL")
            and not values.get("LITELLM_GATEWAY_URL")
        ):
            raise ValueError(
                "Either LITELLM_GATEWAY_URL or TFY_GATEWAY_URL must be set."
            )
        return v

    @field_validator("LITELLM_GATEWAY_API_KEY")
    @classmethod
    def check_litellm_gateway(cls, v, info):
        values = info.data
        if not v and values.get("LITELLM_GATEWAY_URL"):
            raise ValueError(
                "LITELLM_GATEWAY_API_KEY must be set if LITELLM_GATEWAY_URL is provided."
            )
        return v

    @field_validator("TFY_GATEWAY_API_KEY")
    @classmethod
    def check_tfy_gateway(cls, v, info):
        values = info.data
        if not v and values.get("TFY_GATEWAY_URL"):
            raise ValueError(
                "TFY_GATEWAY_API_KEY must be set if TFY_GATEWAY_URL is provided."
            )
        return v

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


settings = Settings()
