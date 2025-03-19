import os
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

PRIMARY_CONFIG = "primary"


class Settings(BaseSettings):
    """
    Settings class to hold all the environment variables
    """

    # Log level can be configured via environment variable, defaults to INFO
    LOG_LEVEL: str = "INFO"
    LITELLM_GATEWAY_URL: str
    LITELLM_GATEWAY_API_KEY: str

    REDIS_URL: str

    PRIMARY_CONFIG: str = PRIMARY_CONFIG
    AGENT_CONFIGS: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "agents"
    )

    # Check if the agent config path exists, if not raise an error, else load the yaml file
    @field_validator("AGENT_CONFIGS")
    @classmethod
    def check_agent_config_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Agent config path {v} does not exist.")
        primary_config_path = os.path.join(v, f"{PRIMARY_CONFIG}.yaml")
        if not os.path.isfile(primary_config_path):
            raise ValueError(
                f"Agent config path {v} does not contain a {PRIMARY_CONFIG}.yaml file. Reading: {primary_config_path}"
            )
        return v

    # Load the yaml file
    @field_validator("AGENT_CONFIGS")
    @classmethod
    def load_agent_configs(cls, v):
        configs = {}
        for file in os.listdir(v):
            if file.endswith(".yaml"):
                with open(os.path.join(v, file), "r") as f:
                    configs[file.replace(".yaml", "")] = yaml.safe_load(f)
        return configs

    def get(self, key_path: str, config_name: str = PRIMARY_CONFIG, default=None):
        """
        Get a value from nested dictionary using dot notation

        Args:
            key_path (str): Path to the key using dot notation (e.g., "checkpointer.type")
            default: Default value if key doesn't exist

        Returns:
            The value at the specified path or the default value
        """
        keys = key_path.split(".")
        value = self.AGENT_CONFIGS[config_name]

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default

        return value if value is not None else default

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


settings = Settings()
