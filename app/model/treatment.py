import datetime

from app.model.watermelon_model import WatermelonModel, ChangeLog, ChangeOperationType
from app.db.database import db
from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy import event
from app.model.model_helper import get_changeset_json, get_epoch_from_datetime, get_datetime_from_epoch


class Treatment(WatermelonModel):
    order_no = db.Column(db.String(255), nullable=False)
    drug_application = db.Column(db.String(255), nullable=False)
    drug_used = db.Column(db.String(255), nullable=False)
    treated_by = db.Column(db.String(255), nullable=False)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    treated_at = db.Column(db.DateTime)
    resaled_at = db.Column(db.DateTime)

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'order_no': self.order_no,
            'drug_used': self.drug_used,
            'drug_application': self.drug_application,
            'treated_by': self.treated_by,
            'start_at': get_epoch_from_datetime(self.start_at),
            'end_at': get_epoch_from_datetime(self.end_at),
            'treated_at': get_epoch_from_datetime(self.treated_at),
            'resaled_at': get_epoch_from_datetime(self.resaled_at)
        }


class TreatmentChangelog(ChangeLog):
    __tablename__ = 'treatment_changelog'


@event.listens_for(Treatment.drug_used, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Treatment.drug_application, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Treatment.treated_by, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Treatment.order_no, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Treatment.start_at, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Treatment.end_at, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Treatment.treated_at, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Treatment.resaled_at, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Treatment, 'before_delete')
def receive_before_delete(mapper, connection, target: Treatment):
    changelog_entry = TreatmentChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                         old_value=str(target.serialize()))
    db.session.add(changelog_entry)


def create_changelog_update_entry(watermelon_id: str, key: str, old_value: str, new_value: str):
    changelog_entry = TreatmentChangelog(operation=ChangeOperationType.UPDATE, watermelon_id=watermelon_id,
                                         old_value=get_changeset_json(key, old_value, new_value))
    db.session.add(changelog_entry)
