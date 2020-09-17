from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity,
    jwt_optional,
    fresh_jwt_required,
)
from models.payment import Payment


class PaymentController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "orderId", type=int, required=True, help="Every payment needs a orderId."
    )

    parser.add_argument(
        "method", type=str, required=True, help="Every payment needs a method."
    )

    @jwt_required
    def post(self):

        props = PaymentController.parser.parse_args()

        payment = Payment(**props)
 
        try:
            payment.save()
        except:
            return {"message": "Something was wrong when creating the payment."}, 500
        
        return payment.json(), 201
    

