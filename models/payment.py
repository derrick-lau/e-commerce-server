from db import db
import datetime

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    order = db.relationship("Order")
    orderId = db.Column(db.Integer, db.ForeignKey("orders.id"))
    createAt = db.Column(db.String(255), default=datetime.datetime.utcnow)
    method = db.Column(db.String(255))

    def __init__(self, orderId, method):
        self.orderId = orderId
        self.method = method

    def json(self):
        return {
            "orderId": self.orderId,
            "createAt": self.createAt,
            "method": self.method
        }

    @classmethod
    def findById(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def findByOrderId(cls, _id):
        return cls.query.filter_by(orderId=_id).first()

    @classmethod
    def findAll(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
