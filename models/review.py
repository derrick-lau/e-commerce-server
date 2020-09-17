from db import db

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), default="")
    rate = db.Column(db.Integer, default = 5)
    product = db.relationship("Product")
    user = db.relationship("User")
    productId = db.Column(db.Integer, db.ForeignKey("products.id"))
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, userId, content, rate, productId):
        self.userId = userId
        self.content = content
        self.rate = rate
        self.productId = productId

    def json(self):
        return {
            "id": self.id,
            "name": self.user.findById(self.userId).name,
            "content": self.content,
            "rate": self.rate
        }
    
    @classmethod
    def findReviewByProductIdAndUserId(cls, productId, userId):
        return cls.query.filter_by(productId=productId, userId=userId).first()

    @classmethod
    def findReviewsByProductId(cls, productId):
        return cls.query.filter_by(productId=productId)

    @classmethod
    def findAll(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
