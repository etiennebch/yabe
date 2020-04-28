"""JSON encoding and decoding.
"""
import json
from collections import deque

from werkzeug.exceptions import HTTPException

from api.error.definition import BaseError, ErrorCode, ErrorType
from api.error.serialization import http_exception_as_json
from api.resource import ApiResource


class JSONEncoder(json.JSONEncoder):
    """A custom JSON encoder that supports our API types.
    """

    def default(self, obj):
        """Overrides default implementation of JSON encoder.
        """
        if isinstance(obj, BaseError):
            return obj.as_json()
        if isinstance(obj, HTTPException):
            return http_exception_as_json(obj)
        if isinstance(obj, (ApiResource, ErrorCode, ErrorType)):
            return obj.value
        if isinstance(obj, deque):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
