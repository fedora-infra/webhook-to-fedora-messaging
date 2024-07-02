from flask import Response, Request


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


def validate_request(request: Request, fields=['username']):
    return all(field in request for field in fields)


def unprocessable_entity() -> Response:
    return Response("{'message: 'Unprocessable Entity'}", status=429, mimetype="application/json")


def exclude_from_val(func):
    func._exclude_from_validation = True
    return func
