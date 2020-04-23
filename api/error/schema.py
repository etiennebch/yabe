"""Schema for the JSON representation of an error.
"""
from marshmallow import Schema, post_dump

from api.serialization import field, schema


class InnerErrorSchema(Schema):
    """The schema for the JSON representation of error details.
    """

    status = field.Integer(strict=True, dump_only=True, description="Corresponding HTTP status.")
    code = field.String(dump_only=True, description="Error code.")
    type = field.String(dump_only=True, description="General category of error.")
    message = field.String(dump_only=True, description="An explanation and resolution steps for the error.")
    url = field.String(dump_only=True, description="A link to look for help about the error.")
    parameter = field.String(dump_only=True, description="Parameter that caused the error, when relevant.")

    @post_dump
    def remove_none(self, data, **kwargs):
        """Remove None values.
        For instance, not all errors have to do with a parameter.
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_dump
    def remove_id(self, data, **kwargs):
        """Remove id from the ResourceMixin as it does not make sense in the context of errors..
        """
        return {k: v for k, v in data.items() if k != "id"}


class ErrorSchema(schema.ResourceMixin):
    """The schema for the JSON representation of an error.
    """

    error = field.Nested(InnerErrorSchema, dump_only=True, description="Details of the error.")

    @staticmethod
    def object_name():
        return "error"
