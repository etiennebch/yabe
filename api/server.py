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


def create_app(secret=None):
    """Create the Flask instance.

    :param secret: filepath to the secret configuration json file.
    :type config: string.
    :returns: a configured Flask instance.
    :rtype: flask.Flask.
    """
    app = Flask(__name__.split(".")[0], root_path=__name__.split(".")[0])
    if secret:
        app.config.from_json(secret)

    _register_extensions(app)
    _register_blueprints(app)

    return app
