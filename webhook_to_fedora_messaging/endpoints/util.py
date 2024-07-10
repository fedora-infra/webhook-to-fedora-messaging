from flask import Response, Request, request, abort
from functools import wraps


def not_found() -> Response:
    return Response({'message': 'Not Found'}, status=404, mimetype='application/json')


def success(data: dict) ->Response:
    return Response(data, status=200, mimetype='application/json')


def bad_request() -> Response:
    return Response("{'message': 'Bad Request'}", status=400, mimetype='application/json')


def created(data: dict) -> Response:
    return Response(data, status=201, mimetype='application/json')


def conflict(data: dict) -> Response:
    return Response(data, status=409, mimetype='application/json')


def unprocessable_entity() -> Response:
    return Response("{'message: 'Unprocessable Entity'}", status=429, mimetype="application/json")


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
