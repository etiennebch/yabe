"""Entrypoint to run the api server.
"""
import argparse
import os

from api.server import create_app


def run(secret):
    """Run the API server.
    """
    app = create_app(secret)
    app.run(debug=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the api server.", prog="yabe")
    parser.add_argument("--secret", help="The path to the secret configuration file.", required=True)
    ns = parser.parse_args()
    run(os.path.abspath(ns.secret))
