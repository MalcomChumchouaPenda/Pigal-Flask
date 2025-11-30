
import os
import sys

current_dir = os.path.dirname(__file__)
examples_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(examples_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)


from flask import Flask
from pigal_flask import Pigal


app = Flask(__name__)
pigal = Pigal(app)


@app.route('/')
def index():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)
