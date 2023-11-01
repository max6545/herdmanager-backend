import datetime

from app.model.watermelon_model import WatermelonModel, ChangeLog, ChangeOperationType
from app.db.database import db
from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy import event
from app.model.model_helper import get_changeset_json
from app.model.model_helper import get_changeset_json, get_epoch_from_datetime, get_datetime_from_epoch


class Treatment(WatermelonModel):
    order_no = db.Column(db.String(255))
    drug_application = db.Column(db.String(255))
    drug_used = db.Column(db.String(255))
    treated_by = db.Column(db.String(255))
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    treated_at = db.Column(db.DateTime)
    resaled_at = db.Column(db.DateTime)

    def serialize(self):
        return str({
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'order_no': self.order_no,
            'drug_used': self.drug_used,
            'drug_application': self.drug_application,
            'treated_by': self.treated_by,
            'start_at': get_epoch_from_datetime(self.start_at),
            'end_at': get_epoch_from_datetime(self.end_at),
            'treated_at': get_epoch_from_datetime(self.treated_at),
            'resaled_at': get_epoch_from_datetime(self.resaled_at)
        })

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

    @staticmethod
    def create_from_json(object_json, farm_id, last_pulled_at, migration_number: int = 11):
        treatment = Treatment(object_json=object_json, farm_id=farm_id, last_pulled_at=last_pulled_at)
        treatment.order_no = object_json['order_no']
        treatment.drug_used = object_json['drug_used']
        treatment.drug_application = object_json['drug_application']
        treatment.treated_by = object_json['treated_by']
        treatment.start_at = get_datetime_from_epoch(object_json['start_at'])
        treatment.end_at = get_datetime_from_epoch(object_json['end_at'])
        treatment.treated_at = get_datetime_from_epoch(object_json['treated_at'])
        treatment.resaled_at = get_datetime_from_epoch(object_json['resaled_at'])
        return treatment

    def update_from_json(self, treatment_json, migration_number: int = 11, last_pulled_at=datetime.datetime.now()):
        WatermelonModel.update_from_json(self, treatment_json, migration_number, last_pulled_at)
        if self.order_no != treatment_json['order_no']:
            self.order_no = treatment_json['order_no']
        if self.drug_application != treatment_json['drug_application']:
            self.drug_application = treatment_json['drug_application']
        if self.drug_used != treatment_json['drug_used']:
            self.drug_used = treatment_json['drug_used']
        if self.treated_by != treatment_json['treated_by']:
            self.treated_by = treatment_json['treated_by']
        if self.start_at != get_datetime_from_epoch(treatment_json['start_at']):
            self.start_at = get_datetime_from_epoch(treatment_json['start_at'])
        if self.end_at != get_datetime_from_epoch(treatment_json['end_at']):
            self.end_at = get_datetime_from_epoch(treatment_json['end_at'])
        if self.treated_at != get_datetime_from_epoch(treatment_json['treated_at']):
            self.treated_at = get_datetime_from_epoch(treatment_json['treated_at'])
        if self.resaled_at != get_datetime_from_epoch(treatment_json['resaled_at']):
            self.resaled_at = get_datetime_from_epoch(treatment_json['resaled_at'])


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
