from time import time, mktime
from datetime import datetime


def gen_now_offset() -> int:
    """Generates a timestamp at a current point in time."""
    return int(time() * 1000)


def timestamp_to_datetime(timestamp: float) -> datetime:
    """Converts timestamp to datetime."""
    return datetime.fromtimestamp(timestamp / 1000)


def datetime_to_timestamp(date_time: datetime) -> int:
    """Converts datetime to timestamp."""
    return int(mktime(date_time.timetuple()) * 1000)
