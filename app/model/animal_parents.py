import datetime

from sqlalchemy import event
from app.db.database import db
from app.model.watermelon_model import WatermelonModel, ChangeOperationType, ChangeLog


class AnimalParents(WatermelonModel):
    parent_id = db.Column(db.String(255))
    child_id = db.Column(db.String(255))

    def serialize(self):
        return str({
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'parent_id': self.parent_id,
            'child_id': self.child_id
        })

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'parent_id': self.parent_id,
            'child_id': self.child_id
        }

    @staticmethod
    def create_from_json(object_json, farm_id, last_pulled_at, migration_number: int = 11):
        animal_parents = AnimalParents(object_json=object_json, farm_id=farm_id,last_pulled_at=last_pulled_at)
        animal_parents.parent_id = object_json['parent_id']
        animal_parents.child_id = object_json['child_id']
        return animal_parents

    def update_from_json(self, relation_json, migration_number: int = 11,last_pulled_at=datetime.datetime.now()):
        WatermelonModel.update_from_json(self, relation_json, migration_number, last_pulled_at)
        if self.child_id != relation_json['child_id']:
            self.child_id = relation_json['child_id']
        if self.parent_id != relation_json['parent_id']:
            self.parent_id = relation_json['parent_id']


class AnimalParentsChangelog(ChangeLog):
    __tablename__ = 'animal_parents_changelog'


@event.listens_for(AnimalParents, 'before_delete')
def receive_before_delete(mapper, connection, target: AnimalParents):
    changelog_entry = AnimalParentsChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                             old_value=str(target.serialize()))
    db.session.add(changelog_entry)
