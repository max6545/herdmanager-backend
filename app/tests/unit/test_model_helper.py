import datetime
import json

from app.model.model_helper import get_datetime_from_epoch, get_epoch_from_datetime, get_changeset_json


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
