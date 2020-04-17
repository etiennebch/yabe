"""Serialization and deserialization wrappers around marshmallow types.
"""
from marshmallow import Schema, fields

from api.config import version


class BaseMixin(Schema):
    """A base schema from which to extend other resources.
    """

    id_ = fields.Integer(
        strict=True, data_key="id", dump_only=True, description="The resource unique identifier."
    )


class VersionMixin(Schema):
    """A mixin to include the api version information in schemas.
    """

    api_version = fields.String(default=version.API_VERSION, dump_only=True, description="The api version.")
