"""Class-based error definitions.
"""
from collections import deque
from enum import Enum
from http import HTTPStatus

from api.config import version
from api.resource import ApiResource


class ErrorType(Enum):
    """Supported error types.
    """

    INVALID_REQUEST = "invalid_request"
    API_ERROR = "api_error"


class ErrorCode(Enum):
    """Supported error codes.
    """

    RESOURCE_NOT_FOUND = "resource_not_found"
    REQUIRED_FIELD = "required_field"
    UNKNOWN_FIELD = "unknown_field"
    INVALID_TYPE = "invalid_type"


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
                "type": self.type,
                "status": self.status,
                "code": self.code,
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


class UnknownField(BaseError):
    """Error raised when an unknown field is found in a request payload.
    """

    def __init__(self, field: str):
        """Constructor.

        :param field: the name of the unknown field.
        """
        self.type = ErrorType.INVALID_REQUEST
        self.code = ErrorCode.UNKNOWN_FIELD
        self.status = HTTPStatus.BAD_REQUEST
        self.message = f"Unknown field in request payload: {field}."
        self.parameter = None
        self.url = None
        super().__init__()


class RequiredField(BaseError):
    """Error raised when a required field is not present in the request payload.
    """

    def __init__(self, field: str):
        """Constructor.

        :param field: the name of the required field.
        """
        self.type = ErrorType.INVALID_REQUEST
        self.code = ErrorCode.REQUIRED_FIELD
        self.status = HTTPStatus.BAD_REQUEST
        self.message = f"Missing required field in request payload: {field}."
        self.parameter = None
        self.url = None
        super().__init__()


class InvalidType(BaseError):
    """Error raised when a payload contains a field whose type is not correct.
    """

    def __init__(self, path: deque, expected_type_name: str):
        """Constructor.

        :param field: the name of the required field.
        """
        self.type = ErrorType.INVALID_REQUEST
        self.code = ErrorCode.INVALID_TYPE
        self.status = HTTPStatus.BAD_REQUEST
        self.message = f"Invalid field type at: $.{'.'.join(path)} ({expected_type_name} expected)."
        self.parameter = None
        self.url = None
        super().__init__()
