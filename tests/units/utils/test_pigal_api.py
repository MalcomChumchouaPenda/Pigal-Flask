
from flask_restx import Namespace
from pigal_flask.utils import PigalApi


def test_is_flask_rest_namespace():
    assert issubclass(PigalApi, Namespace)
