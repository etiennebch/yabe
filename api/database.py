"""Database connection configuration and helpers.
As we don't use SQLAlchemy (neither core nor ORM), it makes much more sense to
use the driver directly.
This module focuses on providing the database connection to the flask application.
"""
from contextlib import contextmanager

from flask import g
from psycopg2.extras import RealDictCursor
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
            cursor_factory=RealDictCursor,
        )

        self.pool = ThreadedConnectionPool(minconn, maxconn, **params)
        return app

    @contextmanager
    def cursor(self):
        """Returns a cursor from a thread-local connection for use within the context of a request.
        g is thread-local so g._database_connection is thread-local.
        In psycpopg2, a connection can spawn multiple cursors which are not isolated. Commit and
        rollback takes effect at the connection level and thus affect all statements executed by
        the cursors spawned from that connection.
        The connection is closed/put back to the pool upon teardown.
        If an exception occur, the transaction is rolled back, otherwise it is committed.
        """
        cursor = g._database_connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()


db = Database()
