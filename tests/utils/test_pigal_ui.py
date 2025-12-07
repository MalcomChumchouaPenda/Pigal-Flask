
from flask import Blueprint
from pigal_flask.utils import PigalUi


def test_is_flask_blueprint():
    assert issubclass(PigalUi, Blueprint)
    