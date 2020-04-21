"""Database connection configuration and helpers.
As we don't use SQLAlchemy (neither core nor ORM), it makes much more sense to
use the driver directly.
This module focuses on providing the database connection to the flask application.
"""
from flask import g
from psycopg2.pool import ThreadedConnectionPool


class Database:
    """Represent an instance of the database.
    """

    def init_app(self, app):
        """Initialize the database extension using the Flask app.

        :param app: the flask application.
        :type app: flask.Flask.
        :returns: the configured flask application.
        :rtype: flask.Flask.
        """
        minconn = app.config.get("POOL_MIN_CONNECTONS", 2)
        maxconn = app.config.get("POOL_MAX_CONNECTONS", 6)
        params = dict(
            dbname=app.config["DATABASE_NAME"],
            user=app.config["DATABASE_USER"],
            password=app.config["DATABASE_PASSWORD"],
            host=app.config["DATABASE_HOST"],
            port=app.config["DATABASE_PORT"],
        )

        self.pool = ThreadedConnectionPool(minconn, maxconn, **params)
        return app

    @property
    def connection(self):
        """Returns a thread-local connection for use within the context of a request.
        """
        return g._database_connection.cursor()


db = Database()
