"""Define error handlers.
"""
from http import HTTPStatus

from flask import jsonify
from marshmallow import Schema, fields, post_dump
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
        return jsonify(exception), exception.status
    if isinstance(exception, HTTPException):
        return jsonify(exception), exception.code
    return jsonify(InternalServerError()), HTTPStatus.INTERNAL_SERVER_ERROR
