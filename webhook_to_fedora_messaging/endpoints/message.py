from flask import Blueprint, abort
from ..database import db
from ..models.service import Service
from .parser.parser import msg_parser
from fedora_messaging import api
from webhook_to_fedora_messaging.exceptions import SignatureMatchError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


message_endpoint = Blueprint("message_endpoint", __name__)


@message_endpoint.route("/<service_uuid>", methods=["POST"])
def create_msg(service_uuid):
    """
    Used for creating a new message by sending a post request to /message path
        
        Request Body:
        service_uuid: Service related to message.    
        
    """
    
    try:
        service = db.session.execute(select(Service).where(Service.uuid == service_uuid)).scalar_one()
    except NoResultFound:
        return {'message': 'Service UUID Not Found'}, 404
    
    try:
        msg = msg_parser(service.type, service.token)
    except SignatureMatchError as e:
        return abort(400, {'message': str(e)})
    except ValueError as e:
        return abort(400, {'message': str(e)})

    api.publish(msg)
    return {'status': 'OK', 'message_id': msg.id}
