from pathlib import Path
import yaml
from typing import Dict
from pydantic import ValidationError
from models import AppConfig
from models import ProjectConfig

class ConfigService:

    def __init__(self, path: str = "config.yaml"):
        self.config_path = Path(path).expanduser()
        self.projects_dict: Dict[str, ProjectConfig] = {}

    @property
    def app_config(self) -> AppConfig:
        return self.app_config

    @property
    def projects(self) -> Dict[str, ProjectConfig]:
        return self.projects_dict

    def load_config(self) -> AppConfig:

        with self.config_path.open("r", encoding="utf-8") as f:
            raw_content = yaml.safe_load(f)

        try:
            self.app_config = AppConfig(**raw_content)

            # Create a project dictionary using the repo as the key
            self.projects_dict = {p.repo: p for p in self.app_config.projects}

            return self.app_config

        except ValidationError as e:
            print("❌ Invalid configuration:")
            print(e)
            raise
