"""Custom marshmallow fields.
"""
from datetime import datetime

from marshmallow import fields
from marshmallow.exceptions import ValidationError


class CustomErrorMessageMixin:
    """A mixin to override the default error values returned by marshmallow field validation.
    """

    default_error_messages = {
        "null": "field may not be null.",
        "required": "field is required.",
        "validator_failed": "field is invalid.",
    }


class Integer(CustomErrorMessageMixin, fields.Integer):
    """Add custom error messages to fields.Integer.
    """


class String(CustomErrorMessageMixin, fields.String):
    """Add custom error messages to fields.String.
    """


class Decimal(CustomErrorMessageMixin, fields.Decimal):
    """Add custom error messages to fields.Decimal.
    """


class Nested(CustomErrorMessageMixin, fields.Nested):
    """Add custom error messages to fields.Nested.
    """


class UInt32LE(fields.Integer):
    """Custom field that deserializes an uint32 integer into bytes using little endian
    representation and serializes the bytes back to an uint32 integer.
    """

    default_error_messages = {"overflow": "number too large."}

    def _serialize(self, value, *args, **kwargs):
        """Override parent _serialize method.
        """
        return int.from_bytes(value, byteorder="little")

    def _deserialize(self, *args, **kwargs):
        """Override parent _deserialize method.
        """
        int_value = super()._deserialize(*args, **kwargs)
        try:
            return int_value.to_bytes(4, byteorder="little", signed=False)
        except OverflowError as error:
            raise self.make_error("overflow") from error


class BinaryHexString(fields.String):
    """Custom field that deserializes an hexadecimal string into a bytearray and serializes a bytearray into an hexadecimal string.
    By hexadecimal string we mean an hexadecimal representation of some underlying data as string.
    """

    default_error_messages = {"invalid": "invalid hexadecimal string."}

    def _serialize(self, value, *args, **kwargs):
        """Override parent _serialize method.
        """
        return value.hex()

    def _deserialize(self, *args, **kwargs):
        """Override parent _deserialize method.
        """
        string_value = super()._deserialize(*args, **kwargs)
        try:
            return bytearray.fromhex(string_value)
        except ValueError as error:
            raise self.make_error("invalid") from error
