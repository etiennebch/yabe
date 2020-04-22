"""Configuration classes for logging.
"""
import logging
from abc import abstractproperty
from logging.config import dictConfigClass

_base_dict = {
    "version": 1,
    "incremental": False,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {"format": '%(levelname)s [%(asctime)s] "%(message)s"', "datefmt": "%Y-%m-%dT%H:%M:%S",}
    },
    "filters": {},
    "handlers": {
        "null": {"class": "logging.NullHandler", "level": logging.DEBUG},
        "console": {
            "class": "logging.StreamHandler",
            "level": logging.DEBUG,
            "formatter": "default",
            "filters": [],
        },
    },
    "loggers": {},
    "root": {"level": logging.DEBUG, "filters": [], "handlers": []},
}


class BaseConfig:
    """A base logging configuration class.
    """

    @property
    @abstractproperty
    def config_dict(self):
        """Must return a configuration dict to use for logging according to the configuration dict schema.
        https://docs.python.org/3.8/library/logging.config.html#configuration-dictionary-schema
        """

    def configure(self):
        """Configure logging according to this configuration.
        """
        dictConfigClass(self.config_dict).configure()


class LocalConfig(BaseConfig):
    """Local logging confuguration.
    """

    def __init__(self, app_name):
        """Initialize the local logging configuration.

        :param name: the name of the flask application.
        :type name: string.
        """
        self.conf = _base_dict
        self.conf["loggers"].update(
            {app_name: {"level": logging.DEBUG, "propagate": False, "filters": [], "handlers": ["console"]}}
        )
        logging.getLogger("werkzeug").disabled = True

    @property
    def config_dict(self):
        return self.conf
