import re
import shutil
import py7zr
from pathlib import Path

from models import AppParams, AppConfig


class DeployService:
    def __init__(self, app_config: AppConfig):
        self.app_config = app_config
        self.app_params: AppParams | None = None

    def deploy(self, app_params: AppParams):
        """Deploy our release artifact to the target directory."""

        self.app_params = app_params

        # Create the location where we will download the deployment artifact
        self.app_config.projects[0].download_directory.mkdir(parents=True, exist_ok=True)
        artifact_source_path = (self.app_config.projects[0].download_directory / "release.7z").expanduser()

        # Make sure directory exists, clear if necessary
        self.app_config.websites_base_path.mkdir(parents=True, exist_ok=True)

        # Define a regex pattern for files to preserve
        # ^ -> start of string, $ -> end of string
        # re.IGNORECASE makes it case-insensitive
        preserve_pattern = re.compile(r"^Web\.config$", re.IGNORECASE)
        target_path = self.app_config.websites_base_path / self.app_config.projects[0].websites[0]
        target_path.mkdir(parents=True, exist_ok=True)

        # Clear directory, preserving any files that need to stay (i.e. Web.config)
        self.__clear_directory(target_path, preserve_pattern)

        self.__extract_artifact(artifact_source_path, target_path)

    @staticmethod
    def __extract_artifact(source_path: Path, destination_path: Path) -> None:
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