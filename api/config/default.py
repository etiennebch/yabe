"""Default configuration for Flask.
Sensitive and runtime specific values are not on source control and are provided at runtime
using the --secret option.
"""


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

    # SQLAlchemy configuration
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_ENGINE_OPTIONS = {"hide_parameters": True, "pool_size": 5, "pool_recycle": 3600}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Serialization with marshmallow
    NULL_FIELD_MESSAGE = "this field may not be null."
    REQUIRED_FIELD_MESSAGE = "this field is required."
    INVALID_FIELD_MESSAGE = "this field is invalid."

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """SQLALCHEMY_DATABASE_URI variable.
        Assumes the existence of variables loaded from the secret.
        """
        return f"postgresql+psycopg2://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


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
