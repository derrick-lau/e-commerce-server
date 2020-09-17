from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity,
    jwt_optional,
    fresh_jwt_required,
)
from models.review import Review


class ReviewController(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        "content", type=str, required=False, help="Every Review needs a content."
    )

    parser.add_argument(
        "rate", type=str, required=True, help="Every Review needs an rate."
    )

    parser.add_argument(
        "productId", type=int, required=True, help="Every Review needs a productId."
    )

    @jwt_required
    def post(self):

        props = ReviewController.parser.parse_args()
        userId = get_jwt_identity()

        if Review.findReviewByProductIdAndUserId(props["productId"], userId):
            return {"message": "You already left a review of this product"}, 400
        else:
            review = Review(userId, **props)

        try:
            print(review)
            review.save()
        except:
            return {"message": "Something was wrong when creating the store."}, 500

        return review.json(), 201

    

