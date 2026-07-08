
from flask import Flask
from .extensions import pigal
from .config import Config


# create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# initialize Flask extensions
pigal.init_app(app)
