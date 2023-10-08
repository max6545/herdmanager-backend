import json


def get_changeset_json(key: str, old_value: str, new_value: str):
    return json.dumps({
        'key': key,
        'oldValue': old_value,
        'newValue': new_value
    })


