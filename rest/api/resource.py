"""Api resources names.
"""
from enum import Enum


class ApiResource(Enum):
    """Enum of the supported api resources.
    """

    BLOCK = "block"
    ERROR = "error"
    LIST = "list"
