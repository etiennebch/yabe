"""Functions to create and configure the Flask server.
"""
from flask import Flask

from api.blueprint.block.router import block
from api.extension import db


def _register_blueprints(app):
    """Register blueprints on a Flask app.

    :param app: the Flask instance.
    :type app: flask.Flask.
    """
    app.register_blueprint(block)


def _register_extensions(app):
    """Register extensions.
    
    :param app: the Flask instance.
    :type app: flask.Flask.
    """
    db.init_app(app)


def create_app(config=None):
    """Create the Flask instance.

    :param config: the filename to the JSON configuration of the Flask server.
    :type config: string.
    :returns: a configured Flask instance.
    :rtype: flask.Flask.
    """
    app = Flask(__name__.split(".")[0], root_path=__name__.split(".")[0])
    if config:
        app.config.from_json(config)

    _register_extensions(app)
    _register_blueprints(app)

    return app
