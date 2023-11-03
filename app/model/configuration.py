import datetime

from app.model.watermelon_model import WatermelonModel, ChangeLog, ChangeOperationType
from app.db.database import db
from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy import event
from app.model.model_helper import get_changeset_json


class Configuration(WatermelonModel):
    configuration_key = db.Column(db.String(255))
    configuration_type = db.Column(db.String(255))
    configuration_value = db.Column(db.String(255))

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'configuration_key': self.configuration_key,
            'configuration_type': self.configuration_type,
            'configuration_value': self.configuration_value
        }


class ConfigurationChangelog(ChangeLog):
    __tablename__ = 'configuration_changelog'


@event.listens_for(Configuration.configuration_key, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Configuration.configuration_type, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Configuration.configuration_value, 'set')
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
