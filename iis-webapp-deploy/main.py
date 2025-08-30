import sys
import argparse
from typing import List
from pydantic import BaseModel, Field, ValidationError

from models import AppParams
from deploy import DeployService


class IisAspNetDeployApp:
    """
    Main application class which provides the ability to deploy an ASP.NET application to IIS
    """

    def __init__(self) -> None:
        self.deploy_service: DeployService = DeployService()

    def run(self, argv:List[str]) -> None:
        self.app_params = self.__parse_app_params(argv)

        self.deploy_service.deploy(self.app_params)


    @staticmethod
    def __parse_app_params(argv:List[str]) -> AppParams:
        try:
            app_params: AppParams = CommandLineInterface.parse_args(argv)
            return app_params

        except ValidationError as e:
            print("[ERROR] Invalid command line arguments:")
            print (e)
            raise


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


def main(argv) -> int:
    """Main entry point for command line interface"""

    if argv is None:
        argv = sys.argv[1:]

    iis_deploy_app = IisAspNetDeployApp()

    try:
        iis_deploy_app.run(argv)

    except Exception as e:
        print("An error occurred attempting to process the deployment:")
        print (e)
        return 1


if __name__ == "__main__":
    ret_code = main(argv=sys.argv[1:])

    sys.exit(ret_code)
