from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from models.user import User
from blacklist import BLACKLIST

parser = reqparse.RequestParser()

parser.add_argument(
    "username", type=str, required=True, help="please enter a username"
)

parser.add_argument(
    "password", type=str, required=True, help="please enter a password"
)

parser.add_argument(
    "name", type=str, required=False, help="please enter a name"
)

parser.add_argument(
    "address", type=str, required=False, help="please enter a address"
)

class UserRegisterController(Resource):

    def post(self):
        props = parser.parse_args()

        if User.findByUsername(props["username"]):
            return {"message": "A user with the same username already exists."}, 400
        user = User(**props)
        user.hashPassword()
        user.save()
        accessToken = create_access_token(identity=user.id, fresh=True)
        refreshToken = create_refresh_token(user.id)

        return {
            "message": "User created successfully.",
            "accessToken": accessToken, 
            "refreshToken": refreshToken
        }, 201


class UserController(Resource):

    @jwt_required
    @classmethod
    def get(cls, user_id: int):
        user = User.findById(user_id)
        if not user:
            return {"message": "No User Found"}, 404
        return user.json(), 200

    @jwt_required
    @classmethod
    def delete(cls, user_id: int):
        user = User.findById(user_id)
        if not user:
            return {"message": "No User Found"}, 404
        user.delete()
        return {"message": "Deleted User successfully"}, 200


class UserSigninController(Resource):
    def post(self):
        props = parser.parse_args()

        user = User.findByUsername(props["username"])
        ## check passward
        print(user, props["password"])
        if user and user.checkPassword(props["password"]):
            print(props["password"],user.checkPassword(props["password"]))
            accessToken = create_access_token(identity=user.id, fresh=True)
            refreshToken = create_refresh_token(user.id)
            return {"accessToken": accessToken, "refreshToken": refreshToken}, 200

        return {"message": "Wrong username or password"}, 401


class UserSignoutController(Resource):

    ## signout and add the token into the blacklist
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "successfully signed out."}, 200


class TokenRefreshController(Resource):
    @jwt_refresh_token_required
    def post(self):
        currentUser = get_jwt_identity()
        newToken = create_access_token(identity=currentUser, fresh=False)
        return {"accessToken": newToken}, 200
