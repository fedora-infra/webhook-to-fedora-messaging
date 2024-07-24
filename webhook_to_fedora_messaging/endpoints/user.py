from flask import request, Blueprint
from ..database import db
from ..models.user import User
from sqlalchemy_helpers import get_or_create
from .util import validate_request


user_endpoint = Blueprint("user_endpoint", __name__, url_prefix="/user")


@user_endpoint.route("/", methods=["POST"])
@validate_request
def create_user():
    """Used for creating a new user by sending a post request to /user/ path.

        Request Body:
            username: Username of the user
            
    """
    user, is_created = get_or_create(db.session, User, username=request.json['username'])
    db.session.commit()
    if not is_created:
        return {'message': 'User Already Exists'}, 409
    else:
        return {'uuid': user.uuid}, 201
        

@user_endpoint.route("/search", methods=["GET"])
@validate_request
def get_user():
    """Used for retrieving a user by sending a get request to /user/search path.

        Request Body:
            username: Username of the user
            
    """
    users = db.session.query(User).filter(User.username.like(request.json['username'])).all()
    if users is None or users == []:
        return {'message': 'Not Found'}, 404
    else:
        return {'user_list': [{'uuid': user.uuid, 'username': user.username} for user in users]}, 200
    

@user_endpoint.route("/", methods=["GET"])
@validate_request
def lookup_user():
    """Used for searching a user by sending a get request to /user/ path.

        Request Body:
            username: Username of the user
    """
    user = db.session.query(User).filter(User.username == request.json['username']).first()
    if user is None:
        return {'message': 'Not Found'}, 404
    else:
        return {'uuid': user.uuid, 'username': user.username}, 200
