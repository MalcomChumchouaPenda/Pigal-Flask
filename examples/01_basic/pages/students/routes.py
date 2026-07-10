
from flask import render_template
from pigal_flask import Ui


ui = Ui(__file__)

@ui.route('/')
def index():
    return render_template('students-index.html')

