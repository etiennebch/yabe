"""Class-based error definitions.
"""
from http import HTTPStatus

from api.error.schema import ErrorSchema


class BaseError(Exception):
    """A base class to derive api exceptions.
    """

    def as_json(self):
        """Return a schema-compliant JSON representation of the error.
        """
        schema = ErrorSchema()
        return schema.dump(
            {
                "error": {
                    "status": self.status,
                    "code": self.code,
                    "message": self.message,
                    "url": self.url,
                    "parameter": self.parameter,
                }
            }
        )


class ResourceNotFound(BaseError):
    """Error raised when resources are not found.
    """

    def __init__(self, resource_name, id_, parameter=None):
        """Constructor.

        :param resource_name: the name of the resource requested (e.g. block).
        :type resource_name: string.
        :param id_: the id of the missing resource.
        :type id_: integer.
        :param parameter: the parameter that caused the error if any.
        :type parameter: string.
        """
        self.status = HTTPStatus.NOT_FOUND
        self.code = "resource_not_found"
        self.message = f"No such {resource_name}: {id_}."
        self.parameter = parameter
        self.url = None
        super(ResourceNotFound, self).__init__()
