
from flask_restx import Resource
from pigal_flask import PigalApi

api = PigalApi(__file__)

@api.route('/hello')
class HelloApi(Resource):
    def get(self):
        return {'message':'Hello World', 'demo':1}
    
