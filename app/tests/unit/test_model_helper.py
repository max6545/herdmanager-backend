import datetime
import json
import time

from app.model.model_helper import get_datetime_from_epoch, get_epoch_from_datetime, get_changeset_json, \
    get_epoch_from_iso_string


def test_get_datetime_from_epoch():
    epoch = 1591959851225
    ts = get_datetime_from_epoch(epoch)
    assert ts.year == 2020
    assert ts.month == 6
    assert ts.day == 12
    assert ts.hour == 13
    assert ts.minute == 4
    assert ts.second == 11
    assert ts.microsecond == 225000


def test_get_epoch_from_datetime():
    dt = datetime.datetime(2020, 6, 12, 13, 4, 11, 225000)
    epoch = get_epoch_from_datetime(dt)
    assert epoch == 1591959851225


def test_get_changeset_json():
    json_data = json.loads(get_changeset_json(key='KEY', old_value='OLD_VALUE', new_value='NEW_VALUE'))
    assert "key" in json_data
    assert json_data["key"] == "KEY"
    assert "oldValue" in json_data
    assert json_data["oldValue"] == "OLD_VALUE"
    assert "newValue" in json_data
    assert json_data["newValue"] == "NEW_VALUE"


def test_get_epoch_from_is_string():
    epoch = get_epoch_from_iso_string("2023-12-11T19:48:33Z")
    assert epoch == 1702320513000
    epoch = get_epoch_from_iso_string("2023-12-11T19:48:33.123Z")
    assert epoch == 1702320513123

    epoch1 = get_epoch_from_iso_string("2023-12-11T19:48:33+01:00")
    assert epoch1 == 1702320513000
    epoch1 = get_epoch_from_iso_string("2023-12-11T19:48:33.836+01:00")
    assert epoch1 == 1702320513836
