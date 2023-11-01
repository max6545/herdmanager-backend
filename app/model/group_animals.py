from sqlalchemy import event
from app.db.database import db
from app.model.watermelon_model import WatermelonModel, ChangeOperationType, ChangeLog
import datetime


class GroupAnimals(WatermelonModel):
    animal_id = db.Column(db.String(255))
    group_id = db.Column(db.String(255))

    def serialize(self):
        return str({
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'group_id': self.group_id,
            'animal_id': self.animal_id
        })

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'group_id': self.group_id,
            'animal_id': self.animal_id
        }

    @staticmethod
    def create_from_json(object_json, farm_id, last_pulled_at, migration_number: int = 11):
        group_animals = GroupAnimals(object_json=object_json, farm_id=farm_id, last_pulled_at=last_pulled_at)
        group_animals.animal_id = object_json['animal_id']
        group_animals.group_id = object_json['group_id']
        return group_animals

    def update_from_json(self, relation_json, migration_number: int = 11, last_pulled_at=datetime.datetime.now()):
        WatermelonModel.update_from_json(self, relation_json, migration_number, last_pulled_at)

        if self.group_id != relation_json['group_id']:
            self.group_id = relation_json['group_id']
        if self.animal_id != relation_json['animal_id']:
            self.animal_id = relation_json['animal_id']


class GroupAnimalsChangelog(ChangeLog):
    __tablename__ = 'group_animals_changelog'


@event.listens_for(GroupAnimals, 'before_delete')
def receive_before_delete(mapper, connection, target: GroupAnimals):
    changelog_entry = GroupAnimalsChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                            old_value=str(target.serialize()))
    db.session.add(changelog_entry)
