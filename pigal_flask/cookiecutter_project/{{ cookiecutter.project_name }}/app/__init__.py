
from flask import Flask
from .extensions import db, pigal
from .config import Config


# create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# initialize Flask extensions
db.init_app(app)
pigal.init_app(app)
