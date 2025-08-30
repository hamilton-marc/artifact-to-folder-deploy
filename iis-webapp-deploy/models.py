from pydantic import BaseModel, Field, ValidationError

class AppParams(BaseModel):
    """
    Validated parameters for the application
    """

    app: str = Field(description="Application to deploy")
    env: str = Field(description="The target environment to deploy to")
    run_id: str = Field(default="latest", description="Run id from GithHub Actions to Deploy")

