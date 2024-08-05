from flask import Blueprint, request
from flask_restx import Api, fields, Resource
from sqlalchemy_helpers import get_or_create

from ..database import db
from ..models.user import User
from .util import validate_request


user_endpoint = Blueprint("user_endpoint", __name__, url_prefix="/user")
user_api = Api(user_endpoint, description="User CRUD Operations", title="User Endpoint")
user_namespace = user_api.namespace("user", description="Create and Get User")
user_search_namespace = user_api.namespace("user/search", "Search a User")


user_fields = user_api.model(
    "body",
    {
        "username": fields.String,
    },
)


@user_namespace.route("/")
class UserEndpoint(Resource):
    """Create and get users"""

    @user_namespace.doc(
        responses={
            404: "Not Found",
            400: "Bad Request",
            415: "Unsupported Media Type",
            200: "{'uuid': 'user-uuid', 'username': 'username'}",
        },
        body=user_fields,
    )
    @user_namespace.expect(user_fields)
    @validate_request
    def get(self):
        """Used for retrieving a created user"""
        user = db.session.query(User).filter(User.username == request.json["username"]).first()
        if user is None:
            return {"message": "Not Found"}, 404
        else:
            return {"uuid": user.uuid, "username": user.username}, 200

    @user_namespace.doc(
        responses={
            404: "Not Found",
            400: "Bad Request",
            415: "Unsupported Media Type",
            200: "{'uuid': 'user-uuid', 'username': 'username'}",
        },
        body=user_fields,
    )
    @user_namespace.expect(user_fields)
    @validate_request
    def post(self):
        """Used for creating a new user by sending a post request to /user/ path.

        Request Body:
            username: Username of the user

        """
        user, is_created = get_or_create(db.session, User, username=request.json["username"])
        db.session.commit()
        if not is_created:
            return {"message": "User Already Exists"}, 409
        else:
            return {"uuid": user.uuid}, 201


@user_search_namespace.route("/")
class UserSearchEndpoint(Resource):
    @validate_request
    def get(self):
        """Used for retrieving a user by sending a get request to /user/search path.

        Request Body:
            username: Username of the user

        """
        users = db.session.query(User).filter(User.username.like(request.json["username"])).all()
        if users is None or users == []:
            return {"message": "Not Found"}, 404
        else:
            return {
                "user_list": [{"uuid": user.uuid, "username": user.username} for user in users]
            }, 200
