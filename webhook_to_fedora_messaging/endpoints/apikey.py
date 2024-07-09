from flask import Blueprint, Flask, request, Response, Request
from ..database import db
from ..models.apikey import APIKey
from ..models.user import User
from datetime import datetime
from sqlalchemy_helpers import get_or_create
from .util import not_found, success, bad_request, created, conflict, validate_request, unprocessable_entity


app = Flask(__name__)
apikey_endpoint = Blueprint("apikey_endpoint", __name__)


@apikey_endpoint.route("/apikey", methods=["POST"])
def create_apikey():
    """Used for creating a new service by sending a post request to /service/ path.
        
        Request body:
            username: Username of the user that api key belongs to
            valid_till: Time the api key will be valid until
            name: Name of the api key.
    """
    session = db.Session()
    body = request.json
    if not validate_request(request, fields=['username', 'valid_till', 'name',]):
        return unprocessable_entity()
    
    user = session.query(User).filter(User.username == body['username']).first()
    if user is None:
        return not_found()
    # Can be different parsing here.
    valid_till = datetime.strptime(body['valid_till'], "%Y-%m-%d")
    apikey, is_created = get_or_create(session, APIKey, user_id=user.id, name=body['name'], expiry_date=valid_till)
    
    if not is_created:
        return conflict({'message': 'Key Already Exists'})
    else:
        return created({'message': 'Created', 'uuid': apikey.id, 'code': apikey.token})
        
    
@apikey_endpoint.route("/apikey/search", methods=["GET"])
def list_apikey():
    """Used for listing all api keys by sending a get request to /apikey/search path.
        
        Request body:
            username: Username of the user
    """
    if not validate_request(request):
        return unprocessable_entity()
        
    session = db.Session()
    user = session.query(User).filter(User.username.like(request.json['username'])).first()
    if user is None:
        return not_found()
    
    apikeys = session.query(APIKey).filter(APIKey.user_id == user.id).all()
    
    return success({'apikey_list': apikeys})
    
    
@apikey_endpoint.route("/apikey", methods=["GET"])
def lookup_apikey():
    """Used for searching api keys by sending a get request to /apikey path
        
        Request body:
            uuid: UUID of the apikey
    """
    if not validate_request(request, fields=['uuid']):
        return unprocessable_entity
    
    session = db.Session()
    apikey = session.query(APIKey).filter(APIKey.id == request.json['apikey_uuid']).first()
    
    if apikey is None:
        return not_found()
    else:
        valid_till = datetime.strftime(apikey.expiry_date, "%Y-%m-%d")
        return success({'uuid': apikey.id, 'name': apikey.name, 'valid_till': valid_till, 'valid': not apikey.disabled})  
    

@apikey_endpoint.route("/apikey/revoke", methods=["PUT"])
def revoke_service():
    """Used for revoking an api key by sending a PUT request to /apikey/revoke path.
        
        Request body:
            username: Username of the user that the api key belongs to.
            apikey_uuid: UUID of the api key.
    """
    if not validate_request(request):
        return unprocessable_entity()
    
    session = db.Session()
    user = session.query(User).filter(User.username == request.json['username']).first()
    apikey = session.query(APIKey).filter(APIKey.user_id == user.id and APIKey.id == request.json['apikey_uuid']).first()
    if apikey is None:
        return not_found()
    else:
        apikey.disabled = True
        session.commit()
        return success({'uuid': apikey.id, 'is_valid': not apikey.disabled})




    