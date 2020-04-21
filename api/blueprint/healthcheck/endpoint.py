"""Endpoints for the healthcheck blueprint.
"""
from api.database import db


def ping():
    """Ping the api server and the underlying database to make sure it is alive.
    """
    try:
        db.connection.execute("SELECT 1")
    # TODO: add logging
    except Exception as e:
        return ("", 503)
    return ("", 200)
