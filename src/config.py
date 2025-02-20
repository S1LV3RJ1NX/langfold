from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Settings class to hold all the environment variables
    """

    LITELLM_GATEWAY_URL: str = ""
    LITELLM_GATEWAY_API_KEY: str = ""

    TFY_GATEWAY_URL: str = ""
    TFY_GATEWAY_API_KEY: str = ""

    LOG_LEVEL: str = "DEBUG"

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
