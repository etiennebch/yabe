"""Marshmallow schema for the error blueprint.
"""
from marshmallow import Schema, fields, post_dump

from api import serialization


class ErrorItemSchema(Schema):
    """The schema for the details of an error.
    """

    status = fields.Integer(strict=True, dump_only=True, description="Corresponding HTTP status.")
    code = fields.String(dump_only=True, description="Error code.")
    type = fields.String(dump_only=True, description="General category of error.")
    message = fields.String(dump_only=True, description="An explanation and resolution steps for the error.")
    url = fields.String(dump_only=True, description="A link to look for help about the error.")
    parameter = fields.String(dump_only=True, description="Parameter that caused the error, when relevant.")

    @post_dump
    def remove_none(self, data):
        """Remove None values.
        For instance, not all errors have to do with a parameter.
        """
        return {k: v for k, v in data.items() if v is not None}


class ErrorSchema(serialization.VersionMixin):
    """The schema for the JSON representation of an error.
    """

    error = fields.Nested(ErrorItemSchema)
