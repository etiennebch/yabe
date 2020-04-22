"""Decorators for the api endpoints.
"""
from flask import request


def listable(f):
    """Extract pagination and list parameters from the url and pass it to the endpoint.
    Requires a request context.
    """

    def wrapped(*args, **kwargs):
        pagination = {
            "after": request.args.get("after"),
            "before": request.args.get("before"),
            "limit": request.args.get("limit"),
        }
        return f(*args, **kwargs, pagination=pagination)

    return wrapped
