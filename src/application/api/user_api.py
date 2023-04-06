from application.api.api_init import *
from flask_restful import Resource, fields, marshal_with
from application.models import User

user_fields = {
    'user_id': fields.Integer, 
    'username': fields.String,
    'display_name': fields.String,
    'role': fields.Integer
}

class UserListAPI(Resource):
        
    @marshal_with(user_fields)
    def get(self):
        try:
            user = User.query.all()
        except:
            raise Error(message="Internal Server Error", status_code=500)
        if user is None:
            raise Error(message ="User not found", status_code=404) 
        else:
            return user, 200
        
        

class UserAPI(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        try:
            user = User.query.filter_by(user_id=user_id).one()
        except:
            raise Error(message="Internal Server Error", status_code=500)
        if user is None:
            raise Error(message ="User not found", status_code=404) 
        else:
            return user, 200