from time import time, mktime
from datetime import datetime
from base64 import b64encode
import requests

from .errors import UnknownError, NotFoundError


def gen_now_offset() -> int:
    """Generates a timestamp at a current point in time."""
    return int(time() * 1000)


def timestamp_to_datetime(timestamp: float) -> datetime:
    """Converts timestamp to datetime."""
    return datetime.fromtimestamp(timestamp / 1000)


def datetime_to_timestamp(date_time: datetime) -> int:
    """Converts datetime to timestamp."""
    return int(mktime(date_time.timetuple()) * 1000)


def file_to_base64(path: str) -> bytes:
    """Opens the file and encodes it in base64."""
    with open(path, 'rb') as file:
        raw_bytes = file.read()
        return b64encode(raw_bytes)


def bytes_to_base64(raw_bytes: bytes) -> bytes:
    """Encodes the string in base64."""
    return b64encode(raw_bytes)


def get_video_preview(video_id: str) -> bytes:
    """Returns YouTube video previews as bytes."""
    url = 'https://img.youtube.com/vi/{id}/0.jpg'.format(id=video_id)
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.content
    elif resp.status_code == 404:
        raise NotFoundError('Video not found.')
    else:
        raise UnknownError('Status code: {code}'.format(code=resp.status_code))


def get_url_image(url: str) -> bytes:
    """Returns the image by the link as a bytes."""
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.content
    elif resp.status_code == 404:
        raise NotFoundError('Video not found.')
    else:
        raise UnknownError('Status code: {code}'.format(code=resp.status_code))
