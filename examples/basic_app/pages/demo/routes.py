
from flask import render_template
from pigal_flask import PigalUi


ui = PigalUi(__name__, __file__)


@ui.route('/')
def index():
    return render_template('demo-index.jinja')
