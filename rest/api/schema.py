"""Schema cache for resource validation.
"""
import json

from api.resource import ApiResource


class SchemaStore:
    """Store JSON schemas of the api resources.
    """

    def __init__(self):
        self._store = {}

    def init_app(self, app):
        """Initialize the schema store using the flask extension factory pattern.
        
        :param app: the flask instance.
        :type app: flask.Flask.
        """
        with open("rest/api/blueprint/block/block.schema.json") as f:
            self._store[ApiResource.BLOCK] = json.load(f)
        return app

    @property
    def block(self):
        """Return the block schema.
        """
        return self._store[ApiResource.BLOCK]


store = SchemaStore()
