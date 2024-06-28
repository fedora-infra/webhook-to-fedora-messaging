from flask import Blueprint, Flask, request, Response, Request
from ..database import db
from ..models.user import User
from sqlalchemy_helpers import get_or_create
from .util import success, bad_request, conflict, created, not_found, validate_request, unprocessable_entity


app = Flask(__name__)
user_endpoint = Blueprint("user_endpoint", __name__)


@user_endpoint.route("/user", methods=["POST"])
@validate_request
def create_user():
    """Used for creating a new user by sending a post request to /user/ path.

        Request Body:
            username: Username of the user
            
    """
    session = db.Session()
    user, is_created = get_or_create(session, User, username=request.json['username'])
    if not is_created:
        return conflict({'message': 'User Already Exists'})
    else:
        return created({'message': 'Created', 'uuid': user.id})
        
    
@user_endpoint.route("/user/search", methods=["GET"])
@validate_request
def get_user():
    """Used for retrieving a user by sending a get request to /user/search path.

        Request Body:
            username: Username of the user
            
    """
    session = db.Session()
    users = session.query(User).filter(User.username.like(request.json['username'])).all()
    if users is None or users == []:
        return not_found()
    else:
        return success({'user_list': users})
    
    
@user_endpoint.route("/user", methods=["GET"])
@validate_request
def lookup_user():
    """Used for searching a user by sending a get request to /user/ path.

        Request Body:
            username: Username of the user
    """
    session = db.Session()

    user = session.query(User).filter(User.username == request.json['username']).first()
    if user is None:
        return not_found()
    else:
        return success({'uuid': user.id, 'username': user.username})
