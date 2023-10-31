from app.model.watermelon_model import WatermelonModel, ChangeLog, ChangeOperationType
from app.db.database import db
from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy import event
from app.model.model_helper import get_changeset_json


class Tag(WatermelonModel):
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    icon = db.Column(db.String(255))
    color = db.Column(db.String(255))

    def serialize(self):
        return str({
            'id': self.id,
            'watermelon_id': self.watermelon_id,
            'name': self.name
        })

    def watermelon_representation(self, migration_number: int = 11):
        return {
            'id': self.watermelon_id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color
        }

    @staticmethod
    def create_from_json(object_json, farm_id, last_pulled_at, migration_number: int = 11):
        tag = Tag(object_json=object_json, farm_id=farm_id, last_pulled_at=last_pulled_at)
        tag.name = object_json['name']
        tag.description = object_json['description']
        tag.icon = object_json['icon']
        tag.color = object_json['color']
        return tag

    def update_from_json(self, group_json, migration_number: int = 11):
        if self.name != group_json['name']:
            self.name = group_json['name']
        if self.description != group_json['description']:
            self.description = group_json['description']
        if self.icon != group_json['icon']:
            self.icon = group_json['icon']
        if self.color != group_json['color']:
            self.color = group_json['color']


class TagChangelog(ChangeLog):
    __tablename__ = 'tag_changelog'


@event.listens_for(Tag.color, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)

@event.listens_for(Tag.name, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Tag.description, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Tag.icon, 'set')
def receive_set(target, new_value, old_value, initiator):
    if old_value is not NO_VALUE and target.id is not None:
        create_changelog_update_entry(target.watermelon_id, initiator.key, old_value, new_value)


@event.listens_for(Tag, 'before_delete')
def receive_before_delete(mapper, connection, target: Tag):
    changelog_entry = TagChangelog(operation=ChangeOperationType.DELETE, watermelon_id=target.watermelon_id,
                                   old_value=str(target.serialize()))
    db.session.add(changelog_entry)


def create_changelog_update_entry(watermelon_id: str, key: str, old_value: str, new_value: str):
    changelog_entry = TagChangelog(operation=ChangeOperationType.UPDATE, watermelon_id=watermelon_id,
                                   old_value=get_changeset_json(key, old_value, new_value))
    db.session.add(changelog_entry)
