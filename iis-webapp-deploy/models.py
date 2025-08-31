from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field


class AppParams(BaseModel):
    """
    Validated parameters for the application
    """

    repo: str = Field(description="GitHub repository name of application to deploy")
    site: Optional[str] = Field(default=None, description="The target IIS site to deploy to")
    run_id: str = Field(default="latest", description="Run id from GithHub Actions to Deploy")


class GitHubConfig(BaseModel):
    """
    Base configuration settings for the GitHub API
    """

    base_url: str
    owner: str


class ProjectConfig(BaseModel):
    """
    Base configuration settings for the project
    """

    name: str
    repo: str
    artifact_filename: str
    download_directory: Path
    websites: List[str]
    allowed_branches: List[str]

    # when clearing target directory, keep files which match this pattern
    preserve_regex: str


class AppConfig(BaseModel):
    """
    Validated parameters for the application configuration
    """

    websites_base_path: Path
    temp_extract_path: Path
    github_config: GitHubConfig
    projects: List[ProjectConfig]

