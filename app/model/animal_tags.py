from app.model.watermelon_model import WatermelonModel, ChangeLog, ChangeOperationType
from app.db.database import db
from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy import event
from app.model.model_helper import get_changeset_json


class AnimalTags(WatermelonModel):
    animal_id = db.Column(db.String(255))
    tag_id = db.Column(db.String(255))

    def serialize(self):
        return str({
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'animal_id': self.animal_id,
            'tag_id': self.tag_id
        })

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'animal_id': self.animal_id,
            'tag_id': self.tag_id
        }

    @staticmethod
    def create_from_json(object_json, farm_id, last_pulled_at, migration_number: int = 11):
        tag = AnimalTags(object_json=object_json, farm_id=farm_id, last_pulled_at=last_pulled_at)
        tag.animal_id = object_json['animal_id']
        tag.tag_id = object_json['tag_id']
        return tag

    def update_from_json(self, group_json, migration_number: int = 11):
        if self.tag_id != group_json['tag_id']:
            self.tag_id = group_json['tag_id']
        if self.animal_id != group_json['animal_id']:
            self.animal_id = group_json['animal_id']


class AnimalTagsChangelog(ChangeLog):
    __tablename__ = 'animal_tags_changelog'


@event.listens_for(AnimalTags.animal_id, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(AnimalTags.tag_id, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(AnimalTags, 'before_delete')
def receive_before_delete(mapper, connection, target: AnimalTags):
    changelog_entry = AnimalTagsChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                          old_value=str(target.serialize()))
    db.session.add(changelog_entry)


def create_changelog_update_entry(watermelon_id: str, key: str, old_value: str, new_value: str):
    changelog_entry = AnimalTagsChangelog(operation=ChangeOperationType.UPDATE, watermelon_id=watermelon_id,
                                          old_value=get_changeset_json(key, old_value, new_value))
    db.session.add(changelog_entry)
