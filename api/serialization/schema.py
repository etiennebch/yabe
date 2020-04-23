"""Custom marshmallow schema types.
"""
from abc import abstractstaticmethod

from marshmallow import Schema, fields, post_dump

from api.config import version


class VersionMixin:
    """A mixin to include the api version information in schemas.
    """

    @post_dump
    def add_version(self, data, **kwargs):
        """Add an api_version field to the serialized output.
        """
        data.update({"api_version": version.API_VERSION})
        return data


class ResourceMixin(Schema, VersionMixin):
    """A base schema from which to extend other resources.
    """

    @staticmethod
    @abstractstaticmethod
    def object_name():
        """Should return the object name (e.g. block).
        
        :rtype: string
        """

    @post_dump
    def add_object(self, data, **kwargs):
        """Add an object field to the serialized output.
        """
        data.update({"object": self.object_name().lower()})
        return data

    id_ = fields.Integer(
        strict=True, data_key="id", dump_only=True, description="The resource unique identifier."
    )
    created_at = fields.Integer(
        strict=True,
        as_string=True,
        dump_only=True,
        description="The resource creation time as seconds since UNIX epoch.",
    )
