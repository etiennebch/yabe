"""Define error handlers.
"""
from flask import jsonify


def handle_base_error(exception):
    """An error handler for errors inheriting BaseError.
    """
    return jsonify(exception), exception.status
