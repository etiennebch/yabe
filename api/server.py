"""Functions to create and configure the Flask server.
"""
from flask import Flask
from marshmallow import fields

from api import before, teardown
from api.blueprint.block.router import block
from api.blueprint.healthcheck.router import healthcheck
from api.config.default import LocalConfig
from api.database import db
from api.encoding import JSONEncoder
from api.error.handler import jsonify_error_handler


def _register_blueprints(app):
    """Register blueprints on a Flask app.

    :param app: the Flask instance.
    :type app: flask.Flask.
    :returns: the configured Flask instance.
    :rtype: flask.Flask.
    """
    app.register_blueprint(block)
    app.register_blueprint(healthcheck)
    return app


def _register_database(app):
    """Register extensions.
    
    :param app: the Flask instance.
    :type app: flask.Flask.
    :returns: the configured Flask instance.
    :rtype: flask.Flask.
    """
    db.init_app(app)
    return app


def _configure_marshmallow(app):
    """Configure app-wide marshmallow settings.

    :param app: the Flask instance.
    :type app: flask.Flask.
    :returns: the configured Flask instance.
    :rtype: flask.Flask.
    """
    fields.Field.default_error_messages = {
        "null": app.config["NULL_FIELD_MESSAGE"],
        "required": app.config["REQUIRED_FIELD_MESSAGE"],
        "validator_failed": app.config["INVALID_FIELD_MESSAGE"],
    }
    return app


def _register_error_handlers(app):
    """Register error handlers.
    
    :param app: the Flask instance.
    :type app: flask.Flask.
    :returns: the configured Flask instance.
    :rtype: flask.Flask.
    """
    app.register_error_handler(Exception, jsonify_error_handler)
    return app


def create_app(secret, environment):
    """Create the Flask instance.

    :param secret: filepath to the secret configuration json file.
    :type secret: string.
    :param environment: the environment to use when creating the server.
    :type environment: string.
    :returns: the configured Flask instance.
    :rtype: flask.Flask.
    """
    app = Flask(__name__.split(".")[0], root_path=__name__.split(".")[0])
    app.config.from_json(secret)
    if environment == "local":
        app.config.from_object(LocalConfig(app.config))

    app.json_encoder = JSONEncoder

    _ = _register_database(app)
    _ = _register_blueprints(app)
    _ = _configure_marshmallow(app)
    _ = _register_error_handlers(app)
    _ = app.before_request(before.acquire_database_connection)
    _ = app.teardown_appcontext(teardown.release_database_connection)

    return app
