from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity,
    jwt_optional,
    fresh_jwt_required,
)

from models.wishListProduct import WishListProduct

class WishListProductsController(Resource):
    @jwt_required
    def get(self):

        userId = get_jwt_identity()
        wishListProducts = [wishListProduct.json() for wishListProduct in WishListProduct.findWishProductsByUserId(userId)]

        if wishListProducts:
            return {"wishListProducts": wishListProducts}, 200
        else:
            return {"message": "wishListProducts not found."}, 404

class AlterWishListProductController(Resource):
    @jwt_required
    def post(self, productId: int):

        userId = get_jwt_identity()
        if (WishListProduct.findByUserIdAndProductId(userId, productId)):
            return {"message": "This product is on you wish list"}, 400

        wishListProduct = WishListProduct(userId, productId)
        try:
            wishListProduct.save()
        except:
            return {"message": "Something was wrong when creating the wishListProduct."}, 500
        
        return {"message": "Added to your wishList.", "wishListProduct":wishListProduct.json()}, 201

    @jwt_required
    def delete(self, productId: int):

        userId = get_jwt_identity()
        wishListProduct = WishListProduct.findByUserIdAndProductId(userId, productId)

        if wishListProduct:
            wishListProduct.delete()
            return {"message": "wishListProduct deleted."}, 200
        else:
            return {"message": "wishListProduct not found."}, 404

