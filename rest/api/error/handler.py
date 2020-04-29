"""Define error handlers.
"""
import re
from http import HTTPStatus

from flask import current_app, jsonify
from jsonschema.exceptions import ValidationError
from werkzeug.exceptions import HTTPException, InternalServerError

from api.error.definition import BaseError, InvalidType, RequiredField, UnknownField


def jsonify_error_handler(exception):
    """Error handler that serializes to JSON.
    
    :param exception: the exception to handle.
    :type exception: Exception or a children class.
    :returns: a jsonified Flask response.
    :rtype: flask.Response.
    """
    if isinstance(exception, BaseError):
        if exception.status >= HTTPStatus.INTERNAL_SERVER_ERROR:
            current_app.logger.exception(exception.message)
        else:
            current_app.logger.warning(exception.message)
        return jsonify(exception), exception.status
    if isinstance(exception, HTTPException):
        if exception.code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            current_app.logger.exception(exception.description)
        else:
            current_app.logger.warning(exception.description)
        return jsonify(exception), exception.code
    if isinstance(exception, ValidationError):
        current_app.logger.warning(exception.message)
        return jsonify(_extract_validation_error(exception)), HTTPStatus.BAD_REQUEST
    current_app.logger.exception(str(exception))
    return jsonify(InternalServerError()), HTTPStatus.INTERNAL_SERVER_ERROR


def _extract_validation_error(exception: ValidationError) -> BaseError:
    """Convert a ValidationError into its BaseError representation.
    
    :param exception: the exception to convert.
    """
    # there is currently no way using jsonschema to know what field
    # caused the error except that parsing the error string
    # https://github.com/Julian/jsonschema/issues/119
    if exception.validator == "required":
        regex = r"^'([a-z0-9_]+)' is a required property$"
        pattern = re.compile(regex)
        field = pattern.match(exception.message).group(1)
        return RequiredField(field, exception.path)
    if exception.validator == "additionalProperties" and not exception.validator_value:
        regex = r"^Additional properties are not allowed \('([a-z0-9_]+)' was unexpected\)$"
        pattern = re.compile(regex)
        field = pattern.match(exception.message).group(1)
        return UnknownField(field, exception.path)
    if exception.validator == "type":
        return InvalidType(exception.path, exception.validator_value)
    return InternalServerError()
