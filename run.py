"""Entrypoint to run the api server.
"""
import argparse
import os

from api.server import create_app


def run(secret, environment):
    """Run the API server.
    """
    app = create_app(secret, environment)
    app.run(debug=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the api server.", prog="yabe")
    parser.add_argument(
        "--environment", help="The environment to use to start the server.", choices=["local"], default="local"
    )
    ns = parser.parse_args()
    filepath = os.path.abspath(f"api/config/{ns.environment}.secret.json")
    run(filepath, ns.environment)
