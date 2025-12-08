
from flask_restx import Resource, fields
from pigal_flask import PigalApi
from .models import db, Person


api = PigalApi(__file__)

person_model = api.model('Person', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    "sex": fields.String(required=True)
})

print('\n', type(person_model), person_model)


@api.route('/persons')
class PersonsApi(Resource):

    @api.marshal_list_with(person_model)
    def get(self):
        '''list all persons'''
        return Person.query.all()
    
    @api.expect(person_model)
    @api.marshal_with(person_model)
    def post(self):
        data = api.payload
        new_person = Person(name=data['name'], sex=data['sex'])
        db.session.add(new_person)
        db.session.commit()
        return new_person
    