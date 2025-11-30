
from pigal_flask import PigalUi


ui = PigalUi(__name__)


@ui.route('/')
def index():
    return "Hello World from Demo"
