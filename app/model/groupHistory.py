from sqlalchemy import event
from sqlalchemy.orm.base import NO_VALUE

from app.db.database import db
from app.model.model_helper import get_changeset_json
from app.model.model_helper import get_epoch_from_datetime
from app.model.watermelon_model import WatermelonModel, ChangeLog, ChangeOperationType


class GroupHistory(WatermelonModel):
    changed_at = db.Column(db.DateTime)
    group_id = db.Column(db.String(255), nullable=False)

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'changed_at': get_epoch_from_datetime(self.changed_at),
            'lot_id': self.group_id
        }


class GroupHistoryChangelog(ChangeLog):
    __tablename__ = 'group_history_changelog'


@event.listens_for(GroupHistory.changed_at, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, str(old_value), str(new_value))


@event.listens_for(GroupHistory.group_id, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(GroupHistory, 'before_delete')
def receive_before_delete(mapper, connection, target: GroupHistory):
    changelog_entry = GroupHistoryChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                            old_value=str(target.serialize()))
    db.session.add(changelog_entry)


def create_changelog_update_entry(watermelon_id: str, key: str, old_value: str, new_value: str):
    changelog_entry = GroupHistoryChangelog(operation=ChangeOperationType.UPDATE, watermelon_id=watermelon_id,
                                            old_value=get_changeset_json(key, old_value, new_value))
    db.session.add(changelog_entry)


class GroupHistoryOldMembers(WatermelonModel):
    history_id = db.Column(db.String(255), nullable=False)
    animal_id = db.Column(db.String(255), nullable=False)

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'history_id': self.history_id,
            'animal_id': self.animal
        }

    def serialize(self):
        return {
            'id': self.id,
            'history_id': self.history_id,
            'animal_id': self.animal
        }


class GroupHistoryOldMembersChangelog(ChangeLog):
    __tablename__ = 'group_history_old_members_changelog'


@event.listens_for(GroupHistoryOldMembers, 'before_delete')
def receive_before_delete(mapper, connection, target: GroupHistoryOldMembers):
    changelog_entry = GroupHistoryOldMembersChangelog(operation=ChangeOperationType.DELETE,
                                                      watermelon_id=target.watermelon_id,
                                                      old_value=str(target.serialize()))
    db.session.add(changelog_entry)


class GroupHistoryNewMembers(WatermelonModel):
    history_id = db.Column(db.String(255), nullable=False)
    animal_id = db.Column(db.String(255), nullable=False)

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'history_id': self.history_id,
            'animal_id': self.animal
        }

    def serialize(self):
        return {
            'id': self.id,
            'history_id': self.history_id,
            'animal_id': self.animal
        }


class GroupHistoryNewMembersChangelog(ChangeLog):
    __tablename__ = 'group_history_new_members_changelog'


@event.listens_for(GroupHistoryNewMembers, 'before_delete')
def receive_before_delete(mapper, connection, target: GroupHistoryNewMembers):
    changelog_entry = GroupHistoryNewMembersChangelog(operation=ChangeOperationType.DELETE,
                                                      watermelon_id=target.watermelon_id,
                                                      old_value=str(target.serialize()))
    db.session.add(changelog_entry)
