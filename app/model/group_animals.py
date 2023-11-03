from sqlalchemy import event
from app.db.database import db
from app.model.watermelon_model import WatermelonModel, ChangeOperationType, ChangeLog
import datetime


class GroupAnimals(WatermelonModel):
    animal_id = db.Column(db.String(255))
    group_id = db.Column(db.String(255))

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'group_id': self.group_id,
            'animal_id': self.animal_id
        }


class GroupAnimalsChangelog(ChangeLog):
    __tablename__ = 'group_animals_changelog'


@event.listens_for(GroupAnimals, 'before_delete')
def receive_before_delete(mapper, connection, target: GroupAnimals):
    changelog_entry = GroupAnimalsChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                            old_value=str(target.serialize()))
    db.session.add(changelog_entry)
