
import os
import sys

root_dir = os.path.dirname(__file__)
while 'examples' in root_dir:
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.append(root_dir)


from flask import Flask
from .extensions import db, pigal
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
pigal.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    from services.demo_v0.models import Person
    person1 = Person(id=1, name='Demo A')
    person2 = Person(id=2, name='Demo B')
    db.session.add_all([person1, person2])
    db.session.commit()

    query = db.session.query(Person)
    print('create avec succes', query.all())

