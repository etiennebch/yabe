"""Before request context hooks.
"""
from flask import g

from api.database import db


def acquire_database_connection():
    """Get a database connection from the pool and make it available to the application context.
    """
    g._database_connection = db.pool.getconn()
    return None
