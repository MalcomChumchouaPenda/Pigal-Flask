
import os
import sys

root_dir = os.path.dirname(__file__)
while 'examples' in root_dir:
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.append(root_dir)


from flask import Flask
from .extensions import pigal
from .config import Config

app = Flask(__name__)
print(app.instance_path, app.import_name)
app.config.from_object(Config)
pigal.init_app(app)
