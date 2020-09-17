from flask_restful import Resource, reqparse
from models.store import Store
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity,
    jwt_optional,
    fresh_jwt_required,
)

class StoreController(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "image", type=str, required=True, help="Every store needs an image."
    )

    def get(self, name):

        store = Store.findByName(name)
        if store:
            return store.json()
        return {
            "message": "Store not found."
        }, 404
            

    @jwt_required
    def post(self, name):

        claims = get_jwt_claims()
        print(claims)

        if not claims["isAdmin"]:
            return {
                "message": "you are not admin"
            }, 401

        props = StoreController.parser.parse_args()

        if Store.findByName(name):
            return {
                "message": "A store with the same already exists."
            }, 400
            
        store = Store(name, **props)

        try:
            store.save()

        except:
            return {
                "message": "something was wrong when creating the store."
            }, 500   
            

        return store.json(), 201

    @jwt_required
    def delete(self, name):

        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {
                "message": "you are not admin"
            }, 401

        store = Store.findByName(name)
        if store:
            store.delete()

        return {
            "message": "Store has been deleted."
        }
            

    @jwt_required
    def put(self, name):

        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {
                "message": "you are not admin"
            }, 401

        props = StoreController.parser.parse_args()

        store = Store.findByName(name)

        if store:
            store.image = props["image"]
        else:
            store = Store(name, **props)

        store.save()

        return store.json(), 200


class StoresController(Resource):
    def get(self):
        return {
            "stores": [store.jsonWithoutProducts() for store in Store.findAll()]
        }
            

