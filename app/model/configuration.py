from app.model.watermelon_model import WatermelonModel, ChangeLog, ChangeOperationType
from app.db.database import db
from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy import event
from app.model.model_helper import get_changeset_json


class Configuration(WatermelonModel):
    key = db.Column(db.String(255))
    type = db.Column(db.String(255))
    value = db.Column(db.String(255))

    def serialize(self):
        return str({
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'key': self.key,
            'type': self.type,
            'value': self.value
        })

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'configuratin_key': self.key,
            'configuratin_type': self.type,
            'configuratin_value': self.value
        }

    @staticmethod
    def create_from_json(object_json, farm_id, last_pulled_at, migration_number: int = 11):
        configuration = Configuration(object_json=object_json, farm_id=farm_id, last_pulled_at=last_pulled_at)
        configuration.key = object_json['configuratin_key']
        configuration.type = object_json['configuratin_type']
        configuration.value = object_json['configuratin_value']
        return configuration

    def update_from_json(self, group_json, migration_number: int = 11):
        if self.key != group_json['configuratin_key']:
            self.key = group_json['configuratin_key']
        if self.type != group_json['configuratin_type']:
            self.type = group_json['configuratin_type']
        if self.value != group_json['configuratin_value']:
            self.value = group_json['configuratin_value']


class ConfigurationChangelog(ChangeLog):
    __tablename__ = 'configuration_changelog'


@event.listens_for(Configuration.key, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Configuration.type, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Configuration.value, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Configuration, 'before_delete')
def receive_before_delete(mapper, connection, target: Configuration):
    changelog_entry = ConfigurationChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                             old_value=str(target.serialize()))
    db.session.add(changelog_entry)


def create_changelog_update_entry(watermelon_id: str, key: str, old_value: str, new_value: str):
    changelog_entry = ConfigurationChangelog(operation=ChangeOperationType.UPDATE, watermelon_id=watermelon_id,
                                             old_value=get_changeset_json(key, old_value, new_value))
    db.session.add(changelog_entry)
