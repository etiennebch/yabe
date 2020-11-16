"""Serialization helpers for errors.
"""
from http import HTTPStatus

from werkzeug.exceptions import HTTPException

from api.config import version
from api.error.definition import ErrorType
from api.resource import ApiResource


def http_exception_as_json(exception: HTTPException) -> dict:
    """Serializes an http exception to json.

    :param exception: the exception to serialize.
    :returns: a dictionary representation of the exception.
    """
    return {
        "object": ApiResource.ERROR,
        "api_version": version.API_VERSION,
        "error": {
            "status": exception.code,
            "code": exception.name.lower().replace(" ", "_"),
            "message": exception.description,
            "url": None,
            "parameter": None,
            "type": ErrorType.INVALID_REQUEST
            if exception.code < HTTPStatus.INTERNAL_SERVER_ERROR
            else ErrorType.API_ERROR,
        },
    }
