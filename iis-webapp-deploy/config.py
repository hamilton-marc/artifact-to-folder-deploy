from pathlib import Path
import yaml
from pydantic import ValidationError
from models import AppConfig  # your Pydantic models

class ConfigService:

    def __init__(self, path: str = "config.yaml"):
        self.config_path = Path(path).expanduser()

    def load_config(self) -> AppConfig:

        with self.config_path.open("r", encoding="utf-8") as f:
            raw_content = yaml.safe_load(f)

        try:
            return AppConfig(**raw_content)

        except ValidationError as e:
            print("❌ Invalid configuration:")
            print(e)
            raise
