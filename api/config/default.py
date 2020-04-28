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

    TESTING = False
    DEBUG = True
    ENV = "production"
    SESSION_COOKIE_SECURE = True
    MAX_CONTENT_LENGTH = 32768  # 32Kb

    # Database configuration
    POOL_MIN_CONNECTONS = 2
    POOL_MAX_CONNECTONS = 6

    DEFAULT_LIMIT = 10

    @property
    def API_VERSION(self):
        """The version of the api.
        """
        return version.API_VERSION


class LocalConfig(BaseConfig):
    """Local configuration for Flask.
    """

    TESTING = True
    DEBUG = True
    ENV = "development"
    # TODO: requires HTTPS in local env
    SESSION_COOKIE_SECURE = False


class ProductionConfig(BaseConfig):
    """Production configuration for Flask.
    """
