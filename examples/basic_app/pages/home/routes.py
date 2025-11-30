
from flask import render_template
from pigal_flask import PigalUi


ui = PigalUi(__file__)


@ui.route('/')
def index():
    return render_template('home.html')

