import json
import time
from datetime import datetime


def get_changeset_json(key: str, old_value: str, new_value: str):
    return json.dumps({
        'key': key,
        'oldValue': old_value,
        'newValue': new_value
    })


def get_epoch_from_datetime(datetime: datetime):
    if not datetime:
        return 0
    return (time.mktime(datetime.timetuple()) * 1000) + (datetime.microsecond / 1000)


def get_epoch_from_iso_string(iso_string: str):
    dt = get_datetime_from_iso_string(iso_string)
    return get_epoch_from_datetime(dt)


def get_datetime_from_iso_string(iso_string: str):
    if not iso_string:
        return 0
    iso_string = iso_string.replace('Z', '+01:00')
    return datetime.fromisoformat(iso_string)


def get_datetime_from_epoch(epoch: int):
    return datetime.fromtimestamp(epoch / 1000)
