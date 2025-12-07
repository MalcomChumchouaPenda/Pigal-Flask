
from flask_restx import Api
from pigal_flask.utils import PigalApi


def test_is_flask_rest_api():
    assert issubclass(PigalApi, Api)
    