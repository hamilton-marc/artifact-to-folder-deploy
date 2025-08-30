import re
import shutil
import py7zr
from pathlib import Path

from models import AppParams, AppConfig


class DeployService:
    def __init__(self, app_config: AppConfig):
        self.app_config = app_config
        self.app_params: AppParams | None = None
        self.temp_dir = Path("~/.tmp")
        self.target_dir = Path("output/target")

    def deploy(self, app_params: AppParams):
        """Deploy our release artifact to the target directory."""

        self.app_params = app_params

        # Hard code artifact name for now
        artifact_source_path = (self.temp_dir / "release.7z").expanduser()

        # Make sure directory exists, clear if necessary
        self.target_dir.mkdir(parents=True, exist_ok=True)

        # Define a regex pattern for files to preserve
        # ^ -> start of string, $ -> end of string
        # re.IGNORECASE makes it case-insensitive
        preserve_pattern = re.compile(r"^Web\.config$", re.IGNORECASE)
        self.__clear_directory(self.target_dir, preserve_pattern)

        self.extract_artifact(artifact_source_path, self.target_dir)

    @staticmethod
    def extract_artifact(source_path: Path, destination_path: Path) -> None:
        """Extract a deployment artifact from source_path to the destination_path."""

        with py7zr.SevenZipFile(source_path, mode='r') as archive:
            archive.extractall(path=destination_path)

    @staticmethod
    def __clear_directory(path: Path, keep_pattern=None) -> None:
        for entry in path.iterdir():
            if keep_pattern and keep_pattern.match(entry.name):
                continue

            try:
                if entry.is_file():
                    entry.unlink()
                elif entry.is_dir():
                    shutil.rmtree(entry)
            except PermissionError as e:
                print(f"Unable to delete {entry}: {e}")
                print(f"The path may be still be in use by another process")