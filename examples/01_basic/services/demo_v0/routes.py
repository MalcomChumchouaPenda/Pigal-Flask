
from flask_restx import Resource
from pigal_flask importModuleApi


api = ModuleApi(__file__)

@api.route('/hello')
class HelloApi(Resource):
    def get(self):
        return {'message':'Hello World', 'demo':0}
    