"""Endpoints for the healthcheck blueprint.
"""
from flask import current_app

from api.database import db


def ping():
    """Ping the api server and the underlying database to make sure it is alive.
    """
    with db.cursor() as cursor:
        try:
            cursor.execute("SELECT 1")
        except Exception as e:
            current_app.logger.exception(e)
            return ("", 503)
    current_app.logger.info("healthcheck passed")
    return ("", 200)
