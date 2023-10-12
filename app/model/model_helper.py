import json
from datetime import datetime
import time


def get_changeset_json(key: str, old_value: str, new_value: str):
    return json.dumps({
        'key': key,
        'oldValue': old_value,
        'newValue': new_value
    })


def get_epoch_from_datetime(datetime: datetime):
    return time.mktime(datetime.timetuple()) * 1000


def get_datetime_from_epoch(epoch: int):
    return datetime.fromtimestamp(epoch / 1000)
