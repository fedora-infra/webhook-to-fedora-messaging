from flask.blueprints import Blueprint
from flask import Flask


vain = Blueprint('main', __name__, url_prefix='/main')


# main endpoints(with prefix /main)...
@vain.route('/gey', methods=["GET"])
def index_main():
    return "Hello world from /main/"
# routes without any prefix


default = Blueprint('default', __name__)


@default.route('/')
def index():
    return "Hello world from /"


def create_app():
    main = Flask(__name__)
    main.register_blueprint(vain)
    main.register_blueprint(default)
    return main
