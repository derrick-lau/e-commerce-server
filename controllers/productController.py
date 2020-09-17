from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity,
    jwt_optional,
    fresh_jwt_required,
)
from models.product import Product


class ProductController(Resource):
    parser = reqparse.RequestParser()
    
    parser.add_argument(
        "price", type=float, required=True, help="Every product needs a price."
    )

    parser.add_argument(
        "storeId", type=int, required=True, help="Every product needs a storeId."
    )

    parser.add_argument(
        "image", type=str, required=True, help="Every product needs an image."
    )

    parser.add_argument(
        "description", type=str, required=True, help="Every product needs a description."
    )

    parser.add_argument(
        "isInStock", type=bool, required=True, help="Every product needs a isInStock."
    )

    def get(self, name):
        product = Product.findByProductName(name)
        if product:
            return product.json(), 200
        return {"message": "Product not found."}, 404


    @jwt_required
    def post(self, name):
        claims = get_jwt_claims()
        if not claims["isAdmin"]:
            return {"message": "you are not admin"}, 401

        if Product.findByProductName(name):
            return {"message": "An product with same name already exists."}, 400

        props = ProductController.parser.parse_args()
        product = Product(name, **props)

        try:
            product.save()
        except:
            return {"message": "Something was wrong when creating the store."}, 500

        return product.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims["isAdmin"]:
            return {"message": "you are not admin"}, 401

        product = Product.findByProductName(name)
        if product:
            product.delete()
            return {"message": "Product deleted."}, 200
        return {"message": "Product not found."}, 404

    @jwt_required
    def put(self, name):
        claims = get_jwt_claims()
        if not claims["isAdmin"]:
            return {"message": "you are not admin"}, 401

        props = ProductController.parser.parse_args()

        product = Product.findByProductName(name)

        if product:
            product.price = props["price"]
            product.image = props["image"]
            product.isInStock = props["isInStock"]
            product.description = props["description"]
        else:
            product = Product(name, **props)

        product.save()

        return product.json(), 200


class ProductsController(Resource):
    
    def get(self, storeId: int):
        products = [product.json() for product in Product.findProductsByStoreId(storeId)]
        if products:
            return {"products": products}, 200
        else:
            return {"message": "No products"}, 404

