
from app.extensions import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(1), nullable=False)

    