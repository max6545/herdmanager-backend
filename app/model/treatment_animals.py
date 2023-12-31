import datetime

from sqlalchemy import event
from app.db.database import db
from app.model.watermelon_model import WatermelonModel, ChangeOperationType, ChangeLog


class TreatmentAnimals(WatermelonModel):
    animal_id = db.Column(db.String(255))
    treatment_id = db.Column(db.String(255))

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'treatment_id': self.treatment_id,
            'animal_id': self.animal_id
        }


class TreatmentAnimalsChangelog(ChangeLog):
    __tablename__ = 'treatment_animals_changelog'


@event.listens_for(TreatmentAnimals, 'before_delete')
def receive_before_delete(mapper, connection, target: TreatmentAnimals):
    changelog_entry = TreatmentAnimalsChangelog(operation=ChangeOperationType.DELETE,
                                                watermelon_id=target.watermelon_id,
                                                old_value=str(target.serialize()))
    db.session.add(changelog_entry)
