from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
import os
from db import db
from dotenv import load_dotenv

from blacklist import BLACKLIST
from controllers.userController import UserRegisterController, UserSigninController, UserController, TokenRefreshController, UserSignoutController
from controllers.productController import ProductController, ProductsController
from controllers.storeController import StoreController, StoresController
from controllers.reviewController import ReviewController
from controllers.orderController import ExistingOrderController, NewOrderController
from controllers.paymentController import PaymentController
from controllers.wishListProductController import WishListProductsController, AlterWishListProductController
from controllers.sessionTrolleyController import TrolleyProductsController, AlterTrolleyProductController, AlterTrolleyProductsController


app = Flask(__name__)
load_dotenv(".env")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI") ## put your own database uri in .env
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True 
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  
app.secret_key = "forka"  
api = Api(app)
CORS(app, allow_headers=[
        "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        supports_credentials=True)

bcrypt = Bcrypt(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


# check if user is admin (id==1 the first user)
@jwt.user_claims_loader
def addJwtClaims(_id):  
    if (_id == 1):  
        return {"isAdmin": True}
    else:
        return {"isAdmin": False}


# check if a token is blacklisted
@jwt.token_in_blacklist_loader
def checkJwtBlacklist(decrypted_token):
    return (decrypted_token["jti"] in BLACKLIST) 


# The methods belows are for customizing jwt responses.
@jwt.expired_token_loader
def expiredJwtRes():
    return (
        jsonify({
            "message": "The token has expired.", 
            "error": "The token has expired."
        }), 401,
    )


@jwt.invalid_token_loader
def invalidJwtRes(error):  
    return (
        jsonify({
            "message": "The token is invalid", 
            "error": "The token is invalid."
        }), 401,
    )


@jwt.unauthorized_loader
def missingJwtRes(error):
    return (
        jsonify({
            "description": "A token is missing",
            "error": "A token is missing",
        }), 401,
    )


@jwt.needs_fresh_token_loader
def jwtNotFreshRes():
    return (
        jsonify({
            "description": "The token is not fresh.", 
            "error": "The token is not fresh."
        }), 401,
    )


@jwt.revoked_token_loader
def JwtRevokedRes():
    return (
        jsonify({
            "description": "The token has been revoked.", 
            "error": "The token has been revoked."   
        }), 401,
    )


api.add_resource(StoreController, "/store/<string:name>")
api.add_resource(StoresController, "/stores")
api.add_resource(ProductController, "/product/<string:name>")
api.add_resource(ProductsController, "/products/<int:storeId>")
api.add_resource(WishListProductsController, "/wishList")
api.add_resource(AlterWishListProductController, "/wishList/<int:productId>")
api.add_resource(TrolleyProductsController, "/trolley")
api.add_resource(AlterTrolleyProductController, "/trolley/<int:productId>")
api.add_resource(AlterTrolleyProductsController, "/trolley/all/<int:productId>")
api.add_resource(NewOrderController, "/order")
api.add_resource(ExistingOrderController, "/order/<int:orderId>")
api.add_resource(PaymentController, "/payment")
api.add_resource(ReviewController, "/review")
api.add_resource(UserRegisterController, "/register")
api.add_resource(UserSigninController, "/login")
api.add_resource(TokenRefreshController, "/refresh")
api.add_resource(UserSignoutController, "/logout")
api.add_resource(UserController, "/user/<int:user_id>")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=8080)
    ##  use your own host