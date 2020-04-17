"""Serialization and deserialization wrappers around marshmallow types.
"""
from marshmallow import fields


class Identifier(fields.Integer):
    """An Identifier field to share across our schemas.
    """

    def __init__(self, *args, **kwargs):
        """Constructor.
        """
        super(Identifier, self).__init__(
            *args, strict=True, data_key="id", dump_only=True, description="The resource unique identifier.", **kwargs
        )
