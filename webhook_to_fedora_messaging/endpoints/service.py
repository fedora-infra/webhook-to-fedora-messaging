from flask import Blueprint, Flask, request, Response, Request
from ..database import db
from ..models.service import Service
from ..models.user import User
from sqlalchemy_helpers import get_or_create
from .util import not_found, success, bad_request, created, conflict, validate_request, exclude_from_val, unprocessable_entity


app = Flask(__name__)
service_endpoint = Blueprint("service_endpoint", __name__)


@service_endpoint.route("/service", methods=["POST"])
def create_service():
    """
    Used for creating a new service by sending a post request to /service/ path.
    """
    if not validate_request(request.json, fields=['username', 'type', 'desc', 'name']):
        return unprocessable_entity()
        
    session = db.Session()
    body = request.json
    

    user = session.query(User).filter(User.username == body['username']).first()
    if user is None:
        return not_found()
    
    service, is_created = get_or_create(session, Service, name=body['name'], type=body['type'], desc=body['desc'], user_id=user.id)
    
    if not is_created:
        return conflict({'message': 'Service Already Exists'})
    else:
        return created({'message': 'Created', 'uuid': service.id})
        
    
@service_endpoint.route("/service/search", methods=["GET"])
def list_services():
    """
    Used for listing all services belong to a user by sending a get request to /service/search path
    """
    if not validate_request(request):
        return unprocessable_entity()
    
    session = db.Session()
    user = session.query(User).filter(User.username.like(request.json['username'])).first()
    if user is None:
        return not_found()
    
    services = session.query(Service).filter(Service.user_id == user.id).all()
    
    return success({'service_list': services})
    
    
@service_endpoint.route("/service", methods=["GET"])
def lookup_service():
    """
    Used for retrieving a service by it's uuid by sending a get request
    to the /service path. 
    
    Request Body:
        service_uuid: Service UUID
    """
    if not validate_request(request, ['service_uuid']):
        return unprocessable_entity()
    
    session = db.Session()
    service = session.query(Service).filter(Service.id == request.json['service_uuid']).first()
    
    if service is None:
        return not_found()
    else:
        return success({'uuid': service.id, 'name': service.name, 'type': service.type, 'desc': service.desc})
    
    
@service_endpoint.route("/service/revoke", methods=["PUT"])
def revoke_service():
    """
    Used for revoking a service by sending a PUT request to /service/revoke path.
    
    Request Body:
        service_uuid: Service UUID
        username: Username of the user that servicce belongs to.
    """
    if not validate_request(request, fields=['username', 'service_uuid']):
        return unprocessable_entity()
    
    session = db.Session()
    user = session.query(User).filter(User.username == request.json['username']).first()
    if user is None:
        return not_found()
    
    service = session.query(Service).filter(Service.user_id == user.id).filter(Service.id == request.json['service_uuid']).first()
    if service is None:
        return not_found()
    
    service.disabled = True
    session.commit()

    return success({'uuid': service.id, 'is_valid': not service.disabled})
    
    
@service_endpoint.route("/service", methods=["PUT"])
def update_service():
    """
    Used for updating a service by sending a PUT request to /service path.
    
    Request Body:
        uuid: UUID of the service
        name: Updated name (optional)
        mesg_body: Updated message body (optional)
    
    """
    if not validate_request(request, fields=['uuid', 'name', 'mesg_body']):
        return unprocessable_entity()
    
    session = db.Session()
    service = session.query(Service).filter(Service.id == request.json['uuid']).first()
    if service is None:
        return not_found()
    
    service.name = request.json['name'] if request.json['name'] is not None and request.json['name'] != "" else service.name
    service.desc = request.json['mesg_body'] if request.json['mesg_body'] is not None and request.json['mesg_body'] != "" else service.desc
    session.commit()
    return success({'uuid': service.id, 'name': service.name, 'mesg_body': service.desc, 'is_valid': not service.disabled})
