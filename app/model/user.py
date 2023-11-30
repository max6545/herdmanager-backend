from flask_bcrypt import generate_password_hash, check_password_hash
from app.db.database import db
from app.model.farm import Farm


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(2000), nullable=False, unique=True)
    mobile_devices = db.relationship('MobileDevice', backref='mobile_device')
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'farm': Farm.query.filter_by(id=self.farm_id).first().serialize() if self.farm_id is not None else None

        }

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def create_user(username: str, password: str):
        user = User(name=username, password=password)
        user.hash_password()
        return user
