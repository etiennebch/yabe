"""Serialization helpers for errors.
"""
from api.error.schema import ErrorSchema


def http_exception_as_json(exception):
    """Serializes an http exception to json.

    :param exception: the exception to serialize.
    :type exception: werkzeug.HTTPException.
    :returns: a dictionary representation of the exception.
    :rtype: dict.
    """
    schema = ErrorSchema()
    return schema.dump(
        {
            "error": {
                "status": exception.code,
                "code": exception.name.lower().replace(" ", "_"),
                "message": exception.description,
                "url": None,
                "parameter": None,
            }
        }
    )
