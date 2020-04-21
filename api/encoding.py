"""JSON encoding and decoding.
"""
import json

from api.blueprint.error.definition import BaseError


class JSONEncoder(json.JSONEncoder):
    """A custom JSON encoder that supports our API types.
    """

    def default(self, obj):
        """Overrides default implementation of JSON encoder.
        """
        if isinstance(obj, BaseError):
            return obj.as_json()
        return json.JSONEncoder.default(self, obj)
