import os
from pathlib import Path
import yaml
from typing import Dict
from pydantic import ValidationError
from models import AppConfig
from models import ProjectConfig
from dotenv import load_dotenv

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

    def _ensure_github_token(self):
        if self._app_config.github_token is None:
            self._app_config.github_token = os.environ.get("GITHUB_TOKEN")

    @staticmethod
    def _load_dotenv():
        # Path to the .env file
        env_path = Path(__file__).parent / ".env"

        # Only load if the file exists
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)

    def load_config(self) -> AppConfig:
        """public: Load the application configuration file."""
        with self._config_path.open("r", encoding="utf-8") as f:
            raw_content = yaml.safe_load(f)

        try:
            self._load_dotenv()
            self._app_config = AppConfig(**raw_content)
            self._ensure_github_token()

            # Create a project dictionary using the repo as the key
            self._projects_dict = {p.repo: p for p in self.app_config.projects}

            return self.app_config

        except ValidationError as e:
            print("❌ Invalid configuration:")
            print(e)
            raise
