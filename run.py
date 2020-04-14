"""Entrypoint to run the api server.
"""
from api.server import create_app


def run():
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    run()
