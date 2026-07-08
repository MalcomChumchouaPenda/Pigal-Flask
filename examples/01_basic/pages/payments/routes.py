
from flask import render_template
from pigal_flask import ModuleUi


ui = ModuleUi(__file__)

@ui.route('/')
def index():
    return render_template('payments-index.jinja')
