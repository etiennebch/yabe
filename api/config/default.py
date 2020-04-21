"""Default configuration for Flask.
Sensitive and runtime specific values are not on source control and are provided at runtime
using the --secret option.
"""
from api.config import version


class BaseConfig:
    """Base configuration for Flask.
    """

    def __init__(self, secret):
        """Initialize the configuration.

        :param secret: the secret configuration values (should be loaded before initializing BaseConfig).
        :type secret: dict.
        """
        for k, v in secret.items():
            setattr(self, k, v)

    DEBUG = False
    TESTING = False
    ENV = "poduction"
    SESSION_COOKIE_SECURE = True
    MAX_CONTENT_LENGTH = 32768  # 32Kb

    # Database configuration
    POOL_MIN_CONNECTONS = 2
    POOL_MAX_CONNECTONS = 6

    # Serialization with marshmallow
    NULL_FIELD_MESSAGE = "this field may not be null."
    REQUIRED_FIELD_MESSAGE = "this field is required."
    INVALID_FIELD_MESSAGE = "this field is invalid."

    @property
    def API_VERSION(self):
        """The version of the api.
        """
        return version.API_VERSION


class LocalConfig(BaseConfig):
    """Local configuration for Flask.
    """

    DEBUG = True
    TESTING = True
    ENV = "development"
    # TODO: requires HTTPS in local env
    SESSION_COOKIE_SECURE = False

    # SQLAlchemy configuration
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {"hide_parameters": False}


class ProductionConfig(BaseConfig):
    """Production configuration for Flask.
    """
