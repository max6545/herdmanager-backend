from sqlalchemy import event
from app.db.database import db
from app.model.watermelon_model import WatermelonModel, ChangeOperationType, ChangeLog


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
    def create_from_json(object_json, farm_id, last_pulled_at):
        return GroupAnimals(watermelon_id=object_json['id'], group_id=object_json['group_id'],
                            animal_id=object_json['animal_id'], farm_id=farm_id, created_at=last_pulled_at,
                            last_changed_at=last_pulled_at)

    def update_from_json(self, relation_json):
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
