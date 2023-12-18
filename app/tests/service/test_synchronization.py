import datetime

from app.service.synchronization.service_helper import get_changes, push_data
from app.model.user import User
from app.model.animal import Animal
from app.model.treatment import Treatment
from app.db.database import db
from app.model.model_helper import get_datetime_from_epoch

table_names = ["animal", "event", "group", "lot", "configuration", "treatment", "tag", "group_animals",
               "treatment_animals", "animal_tags", "lot_history", "lot_history_old_members", "lot_history_new_members",
               "group_history", "group_history_old_members", "group_history_new_members"]


def test_initial_pull(app):
    admin_user = User.query.filter_by(name="admin").first()
    changes = get_changes(None, admin_user.id, 11)
    assert len(changes) == len(table_names)
    for table_name in table_names:
        assert table_name in changes
        assert len(changes[table_name]) == 3
        assert "created" in changes[table_name]
        assert len(changes[table_name]["created"]) == 0
        assert "updated" in changes[table_name]
        assert len(changes[table_name]["updated"]) == 0
        assert "deleted" in changes[table_name]
        assert len(changes[table_name]["deleted"]) == 0


def test_create__update_delete_animal(app):
    tablename = 'animal'
    w_id = 'WATERMELON_ID'
    assert Animal.query.count() == 0
    changes = {
        'changes': {
            tablename: {
                'created': [
                    {'id': w_id, '_status': 'created', '_changed': '', 'animal_type': 'SHEEP',
                     'ear_tag': '111111', 'sex': 'F', 'name': None, 'country_code': 'COUNTRY_CODE',
                     'born_at': 1700504203888, 'farm_code': 'FARM_CODE', 'description': '', 'rejected_at': 0,
                     'rejected_reason': '', 'rejected_info': '', 'lot_id': None, 'father_id': None, 'mother_id': None},
                ],
                'updated': [],
                'deleted': []
            }
        },
        'timestamp': 1700504238000.0}
    admin_user = User.query.filter_by(name="admin").first()
    timestamp_now = datetime.datetime.now()
    push_data(json_data=changes['changes'], push_timestamp=timestamp_now, user_id=admin_user.id, schema_version=11)
    assert Animal.query.count() == 1
    animal = Animal.query.first()
    assert animal.animal_type == 'SHEEP'
    assert animal.name == ''
    assert animal.ear_tag == '111111'
    assert animal.watermelon_id == 'WATERMELON_ID'
    assert animal.created_at == timestamp_now
    assert animal.last_changed_at == timestamp_now
    changes = {
        'changes': {
            tablename: {
                'created': [],
                'updated': [
                    {'id': w_id, '_status': 'created', '_changed': 'ear_tag', 'animal_type': 'SHEEP',
                     'ear_tag': '222222', 'sex': 'F', 'name': None, 'country_code': 'COUNTRY_CODE',
                     'born_at': 1700504203888, 'farm_code': 'FARM_CODE', 'description': '', 'rejected_at': 0,
                     'rejected_reason': '', 'rejected_info': '', 'lot_id': None, 'father_id': None, 'mother_id': None}],
                'deleted': []
            }
        },
        'timestamp': 1700504238000.0}
    timestamp_now2 = datetime.datetime.now()
    push_data(json_data=changes['changes'], push_timestamp=timestamp_now2, user_id=admin_user.id, schema_version=11)

    assert Animal.query.count() == 1
    assert animal.animal_type == 'SHEEP'
    assert animal.name == ''
    assert animal.ear_tag == '222222'
    assert animal.watermelon_id == 'WATERMELON_ID'
    assert animal.created_at == timestamp_now
    assert animal.last_changed_at == timestamp_now2

    changes = {
        'changes': {
            tablename: {
                'created': [],
                'updated': [],
                'deleted': [w_id]
            }
        },
        'timestamp': 1700504238000.0}
    timestamp_now2 = datetime.datetime.now()
    push_data(json_data=changes['changes'], push_timestamp=timestamp_now2, user_id=admin_user.id, schema_version=11)

    assert Animal.query.count() == 0


def test_get_created_animal(app):
    assert Animal.query.count() == 0
    admin_user = User.query.filter_by(name="admin").first()
    animal_json = {
        'id': 'WATERMELON_ID', '_status': 'created', '_changed': 'ear_tag', 'animal_type': 'SHEEP',
        'ear_tag': '222222', 'sex': 'F', 'name': None, 'country_code': 'COUNTRY_CODE',
        'born_at': 1700504203888, 'farm_code': 'FARM_CODE', 'description': '', 'rejected_at': 0,
        'rejected_reason': '', 'rejected_info': '', 'lot_id': None, 'father_id': None, 'mother_id': None
    }
    ts1 = get_datetime_from_epoch(1000)
    ts2 = get_datetime_from_epoch(2000)
    ts3 = get_datetime_from_epoch(3000)
    ts4 = get_datetime_from_epoch(3001)

    animal1 = Animal(object_json=animal_json, farm_id=1, last_pulled_at=ts1)
    animal2 = Animal(object_json=animal_json, farm_id=1, last_pulled_at=ts2)
    animal2.last_changed_at = ts3
    db.session.add(animal1)
    db.session.add(animal2)
    db.session.commit()
    assert Animal.query.count() == 2

    changes = get_changes(None, admin_user.id, 11)
    # returns all 2 animals as created
    assert len(changes["animal"]["created"]) == 2
    assert len(changes["animal"]["updated"]) == 0
    # returns animal2 as created
    changes = get_changes(ts1, admin_user.id, 11)
    assert len(changes["animal"]["created"]) == 1
    assert len(changes["animal"]["updated"]) == 0
    # returns animal2 as updated
    changes = get_changes(ts2, admin_user.id, 11)
    assert len(changes["animal"]["created"]) == 0
    assert len(changes["animal"]["updated"]) == 1
    # returns animal2 as updated
    changes = get_changes(ts3, admin_user.id, 11)
    assert len(changes["animal"]["created"]) == 0
    assert len(changes["animal"]["updated"]) == 1
    # returns no animals
    changes = get_changes(ts4, admin_user.id, 11)
    assert len(changes["animal"]["created"]) == 0
    assert len(changes["animal"]["updated"]) == 0


def test_create_update_delete_treatment(app):
    tablename = 'treatment'
    w_id = 'WATERMELON_ID'
    assert Treatment.query.count() == 0
    changes = {
        'changes': {
            tablename: {
                'created': [
                    {'id': w_id, '_status': 'created', '_changed': '', 'order_no': 'ORDER',
                     'drug_application': 'application', 'drug_used': 'USED', 'treated_by': 'me',
                     'start_at': 1700504203888, 'end_at': 1700504203888, 'resaled_at': 1700504203888,
                     'treated_at': 1700504203888, 'reason': 'r1', 'is_template': False},
                ],
                'updated': [],
                'deleted': []
            }
        },
        'timestamp': 1700504238000.0}
    admin_user = User.query.filter_by(name="admin").first()
    timestamp_now = datetime.datetime.now()
    push_data(json_data=changes['changes'], push_timestamp=timestamp_now, user_id=admin_user.id, schema_version=11)
    assert Treatment.query.count() == 1
    treatment = Treatment.query.first()
    assert treatment.order_no == 'ORDER'
    assert treatment.drug_application == 'application'
    assert treatment.watermelon_id == 'WATERMELON_ID'
    assert treatment.created_at == timestamp_now
    assert treatment.last_changed_at == timestamp_now
    assert treatment.treated_by == 'me'
    changes = {
        'changes': {
            tablename: {
                'created': [],
                'updated': [
                    {'id': w_id, '_status': 'created', '_changed': 'treated_by', 'order_no': 'ORDER',
                     'drug_application': 'application', 'drug_used': 'USED', 'treated_by': 'you',
                     'start_at': 1700504203888, 'end_at': 1700504203888, 'resaled_at': 1700504203888,
                     'treated_at': 1700504203888, 'reason': 'r1', 'is_template': False}],
                'deleted': []
            }
        },
        'timestamp': 1700504238000.0}
    timestamp_now2 = datetime.datetime.now()
    push_data(json_data=changes['changes'], push_timestamp=timestamp_now2, user_id=admin_user.id, schema_version=11)

    assert Treatment.query.count() == 1
    assert treatment.order_no == 'ORDER'
    assert treatment.drug_application == 'application'
    assert treatment.watermelon_id == 'WATERMELON_ID'
    assert treatment.treated_by == 'you'
    assert treatment.created_at == timestamp_now
    assert treatment.last_changed_at == timestamp_now2

    changes = {
        'changes': {
            tablename: {
                'created': [],
                'updated': [],
                'deleted': [w_id]
            }
        },
        'timestamp': 1700504238000.0}
    timestamp_now2 = datetime.datetime.now()
    push_data(json_data=changes['changes'], push_timestamp=timestamp_now2, user_id=admin_user.id, schema_version=11)

    assert Treatment.query.count() == 0
