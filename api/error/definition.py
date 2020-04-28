"""Class-based error definitions.
"""
from enum import Enum
from http import HTTPStatus

from api.config import version
from api.resource import ApiResource


class ErrorType(Enum):
    """Supported error types.
    """

    INVALID_REQUEST = "invalid_request"


class ErrorCode(Enum):
    """Supported error codes.
    """

    RESOURCE_NOT_FOUND = "resource_not_found"
    INVALID_PAYLOAD = "invalid_payload"


class BaseError(Exception):
    """A base class to derive api exceptions.
    """

    def as_json(self):
        """Return a schema-compliant JSON representation of the error.
        """
        return {
            "api_version": version.API_VERSION,
            "object": ApiResource.ERROR,
            "error": {
                "type": self.type.value,
                "status": self.status,
                "code": self.code.value,
                "message": self.message,
                "url": self.url,
                "parameter": self.parameter,
            },
        }


class ResourceNotFound(BaseError):
    """Error raised when resources are not found.
    """

    def __init__(self, resource, id_, parameter=None):
        """Constructor.

        :param resource: the resource requested (e.g. block).
        :type resource: ApiResource.
        :param id_: the id of the missing resource.
        :type id_: integer.
        :param parameter: the parameter that caused the error if any.
        :type parameter: string.
        """
        self.type = ErrorType.INVALID_REQUEST
        self.code = ErrorCode.RESOURCE_NOT_FOUND
        self.status = HTTPStatus.NOT_FOUND
        self.message = f"No such {resource.value}: {id_}."
        self.parameter = parameter
        self.url = None
        super().__init__()
