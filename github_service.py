import io
import os
import sys
import zipfile
from pathlib import Path

import requests
from github.PaginatedList import PaginatedList
from github.Workflow import Workflow
from github.WorkflowRun import WorkflowRun

from config_service import ConfigService
from github import Github, Repository

from models import ProjectConfig


class GitHubService:
    def __init__(self, project_config: ProjectConfig, gh_token: str):
        self._project_config = project_config
        self._gh_token = gh_token
        self._github = Github(gh_token)

    def download_latest_artifact(self):
        repo_path = f"{self._project_config.owner}/{self._project_config.repo}"
        repo: Repository.Repository = self._github.get_repo(repo_path)

        # Find the workflow
        workflow: Workflow = repo.get_workflow(self._project_config.workflow_filename)
        if workflow is None:
            raise Exception(f"Workflow {self._project_config.workflow_filename} does not exist")

        # Find the latest successful workflow run
        workflow_runs: PaginatedList[WorkflowRun] = workflow.get_runs(status="success")
        if workflow_runs.totalCount == 0:
            raise Exception(f"No successful workflow runs found for {self._project_config.workflow_filename}")

        latest_run: WorkflowRun = workflow_runs[0]
        deployment_artifact = latest_run.get_artifacts()[0]

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {self._gh_token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        response = requests.get(deployment_artifact.archive_download_url, headers=headers)
        response.raise_for_status()

#       target_filepath = Path(self._project_config.download_directory / self._project_config.artifact_filename)
#       target_filepath.write_bytes(response.content)

        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            zf.extractall(self._project_config.download_directory)

        print(f"Artifact extracted to {self._project_config.download_directory}")
