from app.db.database import db
from app.model.animal import Animal


class Farm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'animal_count': Animal.query.filter_by(farm_id=self.id).count()
        }
