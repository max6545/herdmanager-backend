from sqlalchemy import event
from db.database import db
from model.watermelon_model import WatermelonModel, ChangeOperationType, ChangeLog


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

    def watermelon_representation(self):
        return str({
            'id': self.watermelon_id,
            'parent_id': self.parent_id,
            'child_id': self.child_id
        })


class AnimalParentsChangelog(ChangeLog):
    __tablename__ = 'animal_parents_changelog'


@event.listens_for(AnimalParents, 'before_delete')
def receive_before_delete(mapper, connection, target: AnimalParents):
    changelog_entry = AnimalParentsChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                             old_value=str(target.serialize()))
    db.session.add(changelog_entry)
