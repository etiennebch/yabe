"""Default configuration for Flask.
Sensitive and runtime specific values are not on source control and are provided at runtime
using the --secret option.
"""


class BaseConfig:
    """Base configuration for Flask.
    """

    DEBUG = False
    TESTING = False

    # SQLAlchemy configuration
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_ENGINE_OPTIONS = {"hide_parameters": True, "pool_size": 5, "pool_recycle": 3600}
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(BaseConfig):
    """Local configuration for Flask.
    """

    DEBUG = True
    TESTING = True

    # SQLAlchemy configuration
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {"hide_parameters": False}

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """SQLALCHEMY_DATABASE_URI variable.
        Assumes the existence of several database variables that are configured as secrets separately.
        """
        return f"postgresql+psycopg2://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
