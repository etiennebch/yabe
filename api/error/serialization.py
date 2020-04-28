"""Serialization helpers for errors.
"""
from api.config import version
from api.resource import ApiResource


def http_exception_as_json(exception):
    """Serializes an http exception to json.

    :param exception: the exception to serialize.
    :type exception: werkzeug.HTTPException.
    :returns: a dictionary representation of the exception.
    :rtype: dict.
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
        },
    }
