import re
import shutil
import py7zr
from pathlib import Path

from config import ConfigService
from models import AppParams, AppConfig


class DeployService:
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service

    def deploy(self, app_params: AppParams) -> None:
        """Deploy our release artifact to the target directory."""

        # Get the configuration for the project to be deployed
        target_project = self.config_service.projects[app_params.repo]

        # Create the location where we will download the deployment artifact
        target_project.download_directory.mkdir(parents=True, exist_ok=True)
        artifact_source_path = (target_project.download_directory / "release.7z").expanduser()

        # Make sure directory exists, clear if necessary
        self.config_service.app_config.websites_base_path.mkdir(parents=True, exist_ok=True)

        for site in target_project.websites:
            self.deploy_to_site(artifact_source_path, site, target_project.preserve_regex)

    def deploy_to_site(self, artifact_source_path: Path, site: str, preserve_regex: str = None) -> None:
        keep_pattern = None

        # If specified, do not delete files that match the preserve_regex pattern
        if preserve_regex:
            keep_pattern = re.compile(preserve_regex, re.IGNORECASE)

        target_path = self.config_service.app_config.websites_base_path / site
        target_path.mkdir(parents=True, exist_ok=True)

        # Clear directory, preserving any files that need to stay (i.e. Web.config)
        self.__clear_directory(target_path, keep_pattern)

        # Unzip the release artifact to the site directory
        self.__extract_artifact(artifact_source_path, target_path)

    @staticmethod
    def __extract_artifact(source_path: Path, destination_path: Path) -> None:
        """Extract a deployment artifact from source_path to the destination_path."""

        with py7zr.SevenZipFile(source_path, mode='r') as archive:
            archive.extractall(path=destination_path)

    @staticmethod
    def __clear_directory(path: Path, preserve_pattern=None) -> None:
        for entry in path.iterdir():
            # Do not delete files which match the preserve_pattern regex
            if preserve_pattern and preserve_pattern.match(entry.name):
                continue

            try:
                if entry.is_file():
                    # this performs a "delete" for a file
                    entry.unlink()
                elif entry.is_dir():
                    # recursively removed the directory
                    shutil.rmtree(entry)
            except PermissionError as e:
                print(f"Unable to delete {entry}: {e}")
                print(f"The path may be still be in use by another process")
