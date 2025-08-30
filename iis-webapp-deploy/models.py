from typing import List

from pydantic import BaseModel, Field, ValidationError

class AppParams(BaseModel):
    """
    Validated parameters for the application
    """

    app: str = Field(description="Application to deploy")
    env: str = Field(description="The target environment to deploy to")
    run_id: str = Field(default="latest", description="Run id from GithHub Actions to Deploy")


class GitHubConfig(BaseModel):
    """
    Base configuration settings for the GitHub API
    """

    base_url: str
    token: str
    owner: str


class ProjectConfig(BaseModel):
    """
    Base configuration settings for the project
    """

    name: str
    repo: str
    workflow_filename: str
    download_directory: str
    websites: List[str]
    allowed_branches: List[str]


class AppConfig(BaseModel):
    """
    Validated parameters for the application configuration
    """

    websites_base_path: str
    temp_extract_path: str
    github_config: GitHubConfig
    projects: List[ProjectConfig]

