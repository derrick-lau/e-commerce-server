from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity,
    jwt_optional,
    fresh_jwt_required,
)
import json 

from models.trolleyProduct_session import SessionTrolleyProduct
from models.product import Product

class TrolleyProductsController(Resource):

    @jwt_required
    def get(self):
        userId = get_jwt_identity()
       
        if SessionTrolleyProduct.getTrolleyProducts(userId):

            trolleyProducts = [SessionTrolleyProduct.getTrolleyProducts(userId)[key].json() for key in SessionTrolleyProduct.getTrolleyProducts(userId)]
           
            return {"trolleyProducts": trolleyProducts}, 200 , 

        else:
            return {"message": "trolley products not found."}, 404, 

class AlterTrolleyProductController(Resource):

    @jwt_required
    def post(self, productId: int):
        if not Product.findById(productId):
           
            return {"message": "This product does not exist"}, 404, 

        userId = get_jwt_identity()

        trolleyProduct = SessionTrolleyProduct(productId, 1, userId)

        try:
            trolleyProduct.add()

        except:
            return {"message": "Something was wrong when creating the TrolleyProduct."}, 500, 

        return  {"message": "Added to your trolley .", "trolleyProduct": trolleyProduct.json()}, 201, 


    @jwt_required
    def delete(self, productId: int):
        if not Product.findById(productId):
            return {"message": "This product does not exist"}, 404, 
        else:
            userId = get_jwt_identity()
            trolleyProduct = SessionTrolleyProduct(productId, 1, userId)

            try:
                trolleyProduct.deleteOne()

            except:
                return {"message": "Something was wrong when deleting the TrolleyProduct."}, 500, 

            return {"message": "TrolleyProduct was deleted."}, 200


class AlterTrolleyProductsController(Resource):
    @jwt_required
    def delete(self, productId: int):
        if not Product.findById(productId):
            return {"message": "This product does not exist"}, 404, 
        else:
            userId = get_jwt_identity()

            trolleyProduct = SessionTrolleyProduct(productId, 1, userId)

            try:
                trolleyProduct.deleteAll()

            except:
                return {"message": "Something was wrong when deleting the TrolleyProducts."}, 500, 

            return {"message": "The trolleyProducts were deleted."}, 200, 





