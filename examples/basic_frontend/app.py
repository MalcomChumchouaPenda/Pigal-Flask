
# EXAMPLE COMFIGURATION

import os
import sys

current_dir = os.path.dirname(__file__)
examples_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(examples_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)


# MINIMAL FRONTEND CONFIGURATION

from flask import Flask
from pigal_flask import Pigal


class Config:
    PIGAL_ROOT_DIR = '.'


app = Flask(__name__)
app.config.from_object(Config)
pigal = Pigal(app)

if __name__ == "__main__":
    app.run(debug=True)
