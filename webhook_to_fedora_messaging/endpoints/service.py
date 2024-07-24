from flask import request, abort, Blueprint
from ..database import db
from ..models.service import Service
from ..models.user import User
from sqlalchemy_helpers import get_or_create
from .util import validate_request
import uuid


service_endpoint = Blueprint("service_endpoint", __name__, url_prefix="/service")


@service_endpoint.route("/", methods=["POST"])
@validate_request(['username', 'type', 'desc', 'name'])
def create_service():
    """
    Used for creating a new service by sending a post request to /service/ path.
    """ 
    user = db.session.query(User).filter(User.username == request.json['username']).first()
    if user is None:
        return {'message': 'Not Found'}, 404
    
    service, is_created = get_or_create(db.session, Service, name=request.json['name'], type=request.json['type'], desc=request.json['desc'], user_id=user.id)
    if not is_created:
        return abort(409, {'message': 'Service Already Exists'})
    else:
        db.session.commit()
        return {'message': 'Created', 'uuid': service.uuid, 'token': service.token}, 201
        
        
@service_endpoint.route("/search", methods=["GET"])
@validate_request
def list_services():
    """
    Used for listing all services belong to a user by sending a get request to /service/search path
    """    
    user = db.session.query(User).filter(User.username.like(request.json['username'])).first()
    if user is None:
        return {'message': 'Not Found'}, 404
    services = db.session.query(Service).filter(Service.user_id == user.id).all()
    return {'service_list': [{
            'id': service.uuid,
            'username': user.username,
            'name': service.name,
            'type': service.type,
            'desc': service.desc,
            'disabled': service.disabled
        } for service in services]}, 200
    
    
@service_endpoint.route("/", methods=["GET"])
@validate_request(['service_uuid'])
def lookup_service():
    """
    Used for retrieving a service by it's uuid by sending a get request
    to the /service path. 
    
    Request Body:
        service_uuid: Service UUID
    """
    service = db.session.query(Service).filter(Service.uuid == request.json['service_uuid']).first()
    if service is None:
        return {'message': 'Not Found'}, 404
    else:
        return {'uuid': service.uuid, 'name': service.name, 'type': service.type, 'desc': service.desc}, 200
    
    
@service_endpoint.route("/revoke", methods=["PUT"])
@validate_request(['username', 'service_uuid'])
def revoke_service():
    """
    Used for revoking a service by sending a PUT request to /service/revoke path.
    
    Request Body:
        service_uuid: Service UUID
        username: Username of the user that servicce belongs to.
    """
    user = db.session.query(User).filter(User.username == request.json['username']).first()
    if user is None:
        return {'message': 'Not Found'}, 404
    
    service = db.session.query(Service).filter(Service.user_id == user.id).filter(Service.uuid == request.json['service_uuid']).first()
    if service is None:
        return {'message': 'Not Found'}, 404

    service.disabled = True
    db.session.commit()

    return {'uuid': service.uuid, 'is_valid': not service.disabled}, 200
    
    
@service_endpoint.route("/", methods=["PUT"])
@validate_request(['service_uuid'])
def update_service():
    """
    Used for updating a service by sending a PUT request to /service path.
    
    Request Body:
        uuid: UUID of the service
        name: Updated name (optional)
        mesg_body: Updated message body (optional)
    
    """
    service = db.session.query(Service).filter(Service.uuid == request.json['service_uuid']).first()
    if service is None:
        return {'message': 'Not Found'}, 404
    
    service.name = request.json['name'] if "name" in request.json and request.json['name'] != "" else service.name
    service.desc = request.json['mesg_body'] if "mesg_body" in request.json and request.json['mesg_body'] != "" else service.desc
    db.session.commit()
    return {'uuid': service.uuid, 'name': service.name, 'mesg_body': service.desc, 'is_valid': not service.disabled}, 200


@service_endpoint.route("/token", methods=['POST'])
@validate_request(['service_uuid'])
def refresh_token():
    service = db.session.query(Service).filter(Service.uuid == request.json['service_uuid']).first()
    if service is None:
        return {'message': 'Not Found'}, 404

    service.token = uuid.uuid4().hex
    db.session.commit()
    return {'uuid': service.uuid, 'name': service.name, 'mesg_body': service.desc, 'is_valid': not service.disabled, 'token': service.token}, 200
