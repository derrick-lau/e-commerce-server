from db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    isAdmin = db.Column(db.Boolean, unique=False, default=True)
    name = db.Column(db.String(100), default="User")
    address = db.Column(db.String(255), default="address")
    reviews = db.relationship("Review", lazy="dynamic")

    def __init__(self, username, password, name, address):
        self.username = username
        self.password = password
        self.name = name
        self.address = address

    def json(self):
        return {
            "id": self.id, 
            "username": self.username,
            "name": self.name, 
            "address": self.address
        }

    def hashPassword(self):
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def findByUsername(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def findById(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
