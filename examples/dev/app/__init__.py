
from flask import Flask
from .extensions import route_manager
from .config import Config


# create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# initialize Flask extensions
route_manager.init_app(app)
