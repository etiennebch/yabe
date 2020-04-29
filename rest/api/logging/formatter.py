"""Formatter classes for logging.
"""
import logging
from datetime import date, datetime
from time import struct_time

import pytz


def utc_timetuple(timestamp):
    """Convert the unix timestamp to localized UTC timetuple.
    """
    dt = pytz.utc.localize(datetime.utcfromtimestamp(timestamp))
    # yday calculation: https://docs.python.org/3/library/datetime.html#datetime.datetime.timetuple
    yday = dt.toordinal() - date(dt.year, 1, 1).toordinal() + 1
    return struct_time(
        (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.weekday(), yday, 0, "UTC", 0)
    )


class UTCFormatter(logging.Formatter):
    """A class to format log datetimes as UTC.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def converter(self, timestamp):
        """Override the converter attribute of the formatter class.
        """
        return utc_timetuple(timestamp)
