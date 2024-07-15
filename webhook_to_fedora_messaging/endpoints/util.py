from flask import Response, Request, request, abort
from functools import wraps


def not_found() -> Response:
    return {'message': 'Not Found'}, 404


def bad_request() -> Response:
    return abort(400, 'Bad Request')


def conflict(data: dict) -> Response:
    return abort(409, data)


def validate_request(request: dict, fields=['username']):
    return all(field in request for field in fields)


def unprocessable_entity() -> Response:
    return {'message': 'Unprocessable Entity'}, 429


def validate_request(fields: list = None):
    fields = fields or ["username"]
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if all(field in request.json for field in fields):
                return view(*args, **kwargs)
            else:
                abort(429, "Missing fields")
        return wrapper
    return decorator
