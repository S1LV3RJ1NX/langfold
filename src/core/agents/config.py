import os
from typing import Iterator

import yaml
from src.config import settings


class AgentConfigs:
    """
    Singleton class to manage agent configurations
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_all_configs(settings.CONFIG_DIR)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self._settings = settings

    def load_all_configs(self, config_dir: str) -> str:
        """Load all YAML configurations from the config directory"""
        if not os.path.exists(config_dir):
            raise ValueError(f"Config directory {config_dir} does not exist.")

        configs = {}
        for filename in os.listdir(config_dir):
            if filename.endswith((".yml", ".yaml")):
                file_path = os.path.join(config_dir, filename)
                # Get filename without extension
                name = os.path.splitext(filename)[0]
                with open(file_path, "r") as f:
                    configs[name] = yaml.safe_load(f)

        # Store configs in instance variable
        self.agent_configs = configs

        # Verify primary config exists
        if settings.PRIMARY_CONFIG not in configs:
            raise ValueError(
                f"Primary config file {settings.PRIMARY_CONFIG} not found in {config_dir}"
            )

        return config_dir

    def get_config(self, agent_name: str) -> dict:
        """Get configuration for a specific agent"""
        return self.agent_configs[agent_name]

    @property
    def agents(self) -> Iterator[str]:
        """Get all agent names"""
        return self.agent_configs.keys()

    @property
    def all_agent_configs(self) -> dict:
        """Get all agent configurations"""
        return self.agent_configs

    @property
    def get_primary_config(self) -> dict:
        """Get the primary agent configuration"""
        return self.agent_configs[settings.PRIMARY_CONFIG]


# Create singleton instance
agent_configs = AgentConfigs()
