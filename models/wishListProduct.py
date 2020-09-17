from db import db

class WishListProduct(db.Model):
    __tablename__ = "wishListProducts"

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User")
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))
    product = db.relationship("Product")
    productId = db.Column(db.Integer, db.ForeignKey("products.id"))

    def __init__(self, userId, productId):
        self.userId = userId
        self.productId = productId

    def json(self):
        product = self.product.findById(self.productId)
        return {
            "productId":self.productId,
            "productName":product.productName,
            "image":product.image,
            "store":product.store.storeName,
            "price":product.price,
        }
    
    @classmethod
    def findById(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def findByUserIdAndProductId(cls, userId, productId):
        return cls.query.filter_by(userId=userId, productId=productId).first()

    @classmethod
    def findWishProductsByUserId(cls, userId):
        return cls.query.filter_by(userId=userId)

    @classmethod
    def findAll(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
