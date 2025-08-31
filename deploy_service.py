import re
import shutil
from pathlib import Path

import py7zr

from config_service import ConfigService
from models import AppParams


class DeployService:
    def __init__(self, config_service: ConfigService):
        self._config_service = config_service

    def deploy(self, app_params: AppParams) -> None:
        """public: Deploy our release artifact to the target directory."""

        # Get the configuration for the project to be deployed
        target_project = self._config_service.projects[app_params.repo]

        # Create the location where we will download the deployment artifact
        target_project.download_directory.mkdir(parents=True, exist_ok=True)
        artifact_source_path = (target_project.download_directory / target_project.artifact_filename).expanduser()

        # Make sure directory exists, clear if necessary
        self._config_service.app_config.websites_base_path.mkdir(parents=True, exist_ok=True)

        for site in target_project.websites:
            self._deploy_to_site(artifact_source_path, site, target_project.preserve_regex)

    def _deploy_to_site(self, artifact_source_path: Path, site: str, preserve_regex: str = None) -> None:
        """private: Deploy a given artifact to a given site."""
        keep_pattern = None

        # If specified, do not delete files that match the preserve_regex pattern
        if preserve_regex:
            keep_pattern = re.compile(preserve_regex, re.IGNORECASE)

        target_path = self._config_service.app_config.websites_base_path / site
        target_path.mkdir(parents=True, exist_ok=True)

        # Clear directory, preserving any files that need to stay (i.e. Web.config)
        self._clear_directory(target_path, keep_pattern)

        # Unzip the release artifact to the site directory
        self._extract_artifact(artifact_source_path, target_path)

    @staticmethod
    def _extract_artifact(source_path: Path, destination_path: Path) -> None:
        """private: Extract a deployment artifact from source_path to the destination_path."""

        with py7zr.SevenZipFile(source_path, mode='r') as archive:
            archive.extractall(path=destination_path)

    @staticmethod
    def _clear_directory(path: Path, preserve_pattern=None) -> None:
        """private: Clear the directory and all its contents. Preserve a pattern if provided."""
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
