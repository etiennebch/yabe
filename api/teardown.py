"""Teardown request and app context hooks.
"""
from flask import g

from api.database import db


def release_database_connection(exception, *args, **kwargs):
    """End the current database transaction (either commit or rollback) and release the connection
    back to the pool.
    This coincides with the one connection per thread/request model.
    This must be registered on REQUEST context teardown (and NOT on the app context teardown) to ensure:
    - it is always executed
    - the exception information is available regardless of any registered error handler

    https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.teardown_request

    :param exception: the exception that occur during handling of the request if any.
    :type exception: Exception.
    :rtype: None.
    """
    try:
        if exception:
            g._database_connection.rollback()
        else:
            g._database_connection.commit()
        db.pool.putconn(g._database_connection)
        g.pop("_database_connection")
    except:
        # TODO log
        pass
    return None
