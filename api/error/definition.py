"""Class-based error definitions.
"""
from enum import Enum
from http import HTTPStatus

from api.config import version


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
            "object": "error",
            "error": {
                "type": self.type,
                "status": self.status,
                "code": self.code,
                "message": self.message,
                "url": self.url,
                "parameter": self.parameter,
            },
        }


class InvalidRequestError(BaseError):
    """Error raised for invalid requests.
    This error is for a whole range of requests that are client errors.
    """

    def __init__(self, code, status, message, parameter=None, url=None):
        self.type = ErrorType.INVALID_REQUEST
        self.code = code.value
        self.message = message
        self.parameter = parameter
        self.url = url
        self.status = status
        super().__init__()


class ResourceNotFound(InvalidRequestError):
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
        super().__init__(
            ErrorCode.RESOURCE_NOT_FOUND,
            HTTPStatus.NOT_FOUND,
            f"No such {resource.name}: {id_}.",
            parameter,
            None,
        )
        super(ResourceNotFound, self).__init__()
