from db import db


class Store(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    storeName = db.Column(db.String(255), unique=True)
    image = db.Column(db.String(255))
    products = db.relationship("Product", lazy="dynamic")

    def __init__(self, storeName, image):
        self.storeName = storeName
        self.image = image

    def json(self):
        return {
            "id": self.id,
            "image": self.image,
            "storeName": self.storeName,
            "products": [product.json() for product in self.products.all()],
        }

    def jsonWithoutProducts(self):
        return {
            "id": self.id,
            "image": self.image,
            "storeName": self.storeName,
        }

    @classmethod
    def findById(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def findByName(cls, storeName):
        return cls.query.filter_by(storeName=storeName).first()

    @classmethod
    def findAll(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
