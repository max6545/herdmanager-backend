import datetime

from sqlalchemy import event
from app.db.database import db
from app.model.watermelon_model import WatermelonModel, ChangeOperationType, ChangeLog


class TreatmentAnimals(WatermelonModel):
    animal_id = db.Column(db.String(255))
    treatment_id = db.Column(db.String(255))

    def serialize(self):
        return str({
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'treatment_id': self.treatment_id,
            'animal_id': self.animal_id
        })

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'treatment_id': self.treatment_id,
            'animal_id': self.animal_id
        }

    @staticmethod
    def create_from_json(object_json, farm_id, last_pulled_at, migration_number: int = 11):
        treatment_animals = TreatmentAnimals(object_json=object_json, farm_id=farm_id, last_pulled_at=last_pulled_at)
        treatment_animals.animal_id = object_json['animal_id']
        treatment_animals.treatment_id = object_json['treatment_id']
        return treatment_animals

    def update_from_json(self, update_json, migration_number: int = 11, last_pulled_at=datetime.now()):
        WatermelonModel.update_from_json(self, update_json, migration_number, last_pulled_at)
        if self.treatment_id != update_json['treatment_id']:
            self.treatment_id = update_json['treatment_id']
        if self.animal_id != update_json['animal_id']:
            self.animal_id = update_json['animal_id']


class TreatmentAnimalsChangelog(ChangeLog):
    __tablename__ = 'treatment_animals_changelog'


@event.listens_for(TreatmentAnimals, 'before_delete')
def receive_before_delete(mapper, connection, target: TreatmentAnimals):
    changelog_entry = TreatmentAnimalsChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                                old_value=str(target.serialize()))
    db.session.add(changelog_entry)
