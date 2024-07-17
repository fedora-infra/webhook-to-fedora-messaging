from flask import Response, request, abort
from functools import wraps


def validate_request(fields=None):
    fields = fields or ['username']

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if the request has JSON data
            if not request.is_json:
                return abort(400, {"error": "Invalid input, JSON required"})
            data = request.get_json()
            # Check if all required fields are present
            missing_fields = [field for field in fields if field not in data]
            if missing_fields:
                return abort(400, {"error": f"Missing fields: {', '.join(missing_fields)}"})

            return func(*args, **kwargs)
        return wrapper

    # If the decorator is used without arguments
    if callable(fields):
        func = fields
        fields = ['username']
        return decorator(func)

    return decorator
