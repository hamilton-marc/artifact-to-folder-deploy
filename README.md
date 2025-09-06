# Artifact to Folder Deploy

This project provides a Python application for deploying build artifacts (downloaded from GitHub Actions workflow runs) into IIS websites. It automates the process of fetching artifacts, extracting them, and deploying them to the correct target directories.

The application is written in Python and starts in **`main.py`**.

---

## Features

- Download artifacts directly from GitHub Actions workflow runs
- Support for multiple projects defined in a YAML configuration
- Select target project by repository name
- Optional preservation rules (e.g., keep `Web.config`)
- Cross-platform path handling (`pathlib.Path`)
- Rich console output using [`rich`](https://github.com/Textualize/rich)
- Configuration management with [`pydantic`](https://docs.pydantic.dev/)

---

## Requirements

- Python **3.10+**
- Access to GitHub with a **Personal Access Token** (PAT) or `GITHUB_TOKEN`
- (Optional) Windows Server with IIS installed if deploying to IIS

---

## Installation

```bash
git clone https://github.com/hamilton-marc/artifact-to-folder-deploy.git
cd artifact-to-folder-deploy
pip install -r requirements.txt
```

## Configuration

Here is what a sample configuration might look like:

```yaml
websites_base_path: <<path to your site>>
temp_extract_path: <<temporary path to extract the artifact>>

github_config:
  base_url: "https://api.github.com"
  token: "${GITHUB_TOKEN}"
  owner: "<<GitHub owner name>>"

projects:
  - name: <<name of the project to deploy>>
    repo: <<Name of the GitHub repo containing the artifact>>
    workflow_filename: <<workflow file which contains the artifact>>
    download_directory: <target path to download the artifact>>
    websites:
      - <<site path where to extract the contents of the artifact>>
    allowed_branches:
      - "main"
      - "develop"
```

## Environment Variables

GITHUB_TOKEN should be set in your environment or a local .env (not committed).
Minimum scopes:

Public repos: actions:read

Private repos: repo, actions:read

Example `.env`:

```bash
GITHUB_TOKEN=ghp_your_token_here
```

## Usage

Run the deployment application:

```bash
python main.py --repo my-repo --site "MyAppSite"
```

### Command Line Arguments

- `--repo` (required): GitHub repository name of the project to deploy
- `--site` (optional): Target IIS site to deploy to
- `--run_id` (optional, default: latest): Workflow run ID to pull the artifact from

### Examples:

#### Deploy latest successful run

```bash
python main.py --repo my-repo
```

#### Deploy a specific run
```bash
python main.py --repo my-repo --run_id 123456789
```