"""Define error handlers.
"""
from http import HTTPStatus

from flask import current_app, jsonify
from werkzeug.exceptions import HTTPException, InternalServerError

from api.error.definition import BaseError


def jsonify_error_handler(exception):
    """Error handler that serializes to JSON.
    
    :param exception: the exception to handle.
    :type exception: Exception or a children class.
    :returns: a jsonified Flask response.
    :rtype: flask.Response.
    """
    if isinstance(exception, BaseError):
        if exception.status >= HTTPStatus.INTERNAL_SERVER_ERROR:
            current_app.logger.exception(exception.message)
        else:
            current_app.logger.warning(exception.message)
        return jsonify(exception), exception.status
    if isinstance(exception, HTTPException):
        if exception.code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            current_app.logger.exception(exception.description)
        else:
            current_app.logger.warning(exception.description)
        return jsonify(exception), exception.code
    current_app.logger.exception(str(exception))
    return jsonify(InternalServerError()), HTTPStatus.INTERNAL_SERVER_ERROR
