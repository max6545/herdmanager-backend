from app.model.user import User
from app.model.group import Group
from app.model.animal import Animal
from datetime import datetime


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = User.create_user('admin', 'admin')
    assert user.name == 'admin'
    assert user.password != 'admin'
    assert user.password != ''


def test_new_group(app):
    farm_id = 1
    json_id = '12'
    json_name = 'group_name'

    object_json = {
        'id': json_id,
        'name': json_name
    }
    now = datetime.now()

    group = Group(object_json, farm_id, last_pulled_at=now)
    assert group.watermelon_id == json_id
    assert group.farm_id == farm_id
    assert group.name == json_name
    assert group.last_changed_at == now
    assert group.created_at == now
