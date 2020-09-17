from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity,
    jwt_optional,
    fresh_jwt_required,
)

from models.order import Order
from models.orderProduct import OrderProduct


parser = reqparse.RequestParser()

parser.add_argument(
    "orderProducts", '--list', action='append', type=dict, required=True, help="Every order needs a orderProducts."
)

parser.add_argument(
    "address", type=str, required=True, help="Every order needs a address."
)

class ExistingOrderController(Resource):

    @jwt_required
    def get(self, orderId: int):
        order = Order.findById(orderId)

        if order:
            return order.json(), 200
        else:
            return {"message": "order not found."}, 404

    @jwt_required
    def delete(self, orderId: int):

        order = Order.findById(orderId)

        if order:
            order.delete()
            return {"message": "Order deleted."}, 200
        else:
            return {"message": "Order not found."}, 404


class NewOrderController(Resource):

    @jwt_required
    def get(self):

        userId = get_jwt_identity()
        orders = [order.json() for order in Order.findOrdersByUserId(userId)]

        if orders:
            return {"orders": orders}, 200
        else:
            return {"message": "order not found."}, 404

    @jwt_required
    def post(self):

        props = parser.parse_args()
        userId = get_jwt_identity()
        orderProducts = props['orderProducts']
        order = Order(userId, props['address'])
        try:
            order.save()

            for orderProduct in orderProducts:
                orderProduct = OrderProduct(order.id, orderProduct['productId'], orderProduct['quantity'])
                orderProduct.save()
        except:
            return {"message": "Something was wrong when creating the order."}, 500
        
        return {"message": "order created.", "order":order.json()}, 201
    

