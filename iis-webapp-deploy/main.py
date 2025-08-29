import sys
import argparse
from typing import List, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, ValidationError

class AppParams(BaseModel):
    """
    Validated parameters for the application
    """

    app: str = Field(description="Application to deploy")
    env: str = Field(description="The target environment to deploy to")
    run_id: str = Field(default="latest", description="Run id from GithHub Actions to Deploy")

class Application:
    """
    Base application class with boilerplate implementation to collect command line args
    """

    def __init__(self, args: argparse.Namespace):
        """Constructor. Set up internal member variables"""
        self.args = args

    @abstractmethod
    def run(self) -> None:
        """Derived classes must implement a run method."""
        pass

class IisAspNetDeployApp(Application):
    """
    Main application class which provides the ability to deploy an ASP.NET application to IIS
    """

    def run(self):
        pass

class CommandLineInterface:
    """
    Command line interface to help us parse the arguments
    """

    @staticmethod
    def parse_args(argv: List[str]) -> AppParams:
        """Parse command line arguments"""

        parser = argparse.ArgumentParser(description="IIS ASP.NET Deployment App")

        parser.add_argument(
            "--app",
            type=str,
            help="Application to deploy (must be pre-configured)"
        )
        parser.add_argument(
            "--env",
            type=str,
            help="Target environment to deploy to"
        )
        parser.add_argument(
            "--runid",
            type=str,
            default="latest",
            help="GitHub Actions Run Id"
        )

        raw_args = parser.parse_args(argv)

        # Throws a ValidationException if the args are missing or invalid
        app_params = AppParams(**vars(raw_args))

        return app_params

def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for command line interface
    """

    if argv is None:
        argv = sys.argv[1:]

    try:
        app_params: AppParams = CommandLineInterface.parse_args(argv)

    except ValidationError as e:
        print("[ERROR] Invalid arguments:")
        print(e)
        return 2

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    ret_code = main()

    sys.exit(ret_code)


