"""Endpoints for the healthcheck blueprint.
"""
from flask import current_app

from api.database import db


def ping():
    """Ping the api server and the underlying database to make sure it is alive.
    """
    try:
        db.cursor.execute("SELECT 1")
    except Exception as e:
        current_app.logger.exception(str(e))
        return ("", 503)
    current_app.logger.info("healthcheck passed")
    return ("", 200)
