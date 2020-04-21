"""Teardown request and app context hooks.
"""
from flask import g

from api.database import db


def release_database_connection(*args, **kwargs):
    """Put the database connection back into the pool.
    """
    db.pool.putconn(g._database_connection)
    g.pop("_database_connection")
    return None
