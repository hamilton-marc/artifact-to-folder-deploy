from pathlib import Path
import yaml
from typing import Dict
from pydantic import ValidationError
from models import AppConfig
from models import ProjectConfig

class ConfigService:
    """
    This class is used to parse and manage the application configuration file.
    """
    def __init__(self, path: str = "config.yaml"):
        self._config_path = Path(path).expanduser()
        self._projects_dict: Dict[str, ProjectConfig] = {}
        self._app_config: AppConfig | None = None

    @property
    def app_config(self) -> AppConfig:
        return self._app_config

    @property
    def projects(self) -> Dict[str, ProjectConfig]:
        """public read-only: Returns a dictionary of projects keyed by repo"""
        return self._projects_dict

    def load_config(self) -> AppConfig:
        """public: Load the application configuration file."""
        with self._config_path.open("r", encoding="utf-8") as f:
            raw_content = yaml.safe_load(f)

        try:
            self._app_config = AppConfig(**raw_content)

            # Create a project dictionary using the repo as the key
            self._projects_dict = {p.repo: p for p in self.app_config.projects}

            return self.app_config

        except ValidationError as e:
            print("❌ Invalid configuration:")
            print(e)
            raise
