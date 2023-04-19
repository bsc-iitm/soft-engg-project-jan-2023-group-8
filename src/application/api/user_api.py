from application.api.api_init import *
from flask_restful import Resource, fields, marshal_with,reqparse
from application.models import User
from application.db import db
from datetime import datetime


user_fields = {
    'user_id': fields.Integer, 
    'username': fields.String,
    'email': fields.String,
    'role': fields.Integer,
    'joined_at':fields.DateTime
}

message_parser = reqparse.RequestParser()
message_parser.add_argument('email')
message_parser.add_argument('password')
message_parser.add_argument('role')
message_parser.add_argument('username')


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
       
    @marshal_with(user_fields) 
    def post(self): 
        args = message_parser.parse_args()
        email = args['email']
        password = args['password']
        role=args['role']
        username=args['username']
        
        # Argument Handling
        if role is None or role == '':
            raise Error(message = 'Role is required.', status_code=400)
        if email is None or email == '':
            raise Error(message = 'email is required.', status_code=400)
        if username is None or username == '':
            raise Error(message = 'username is required.', status_code=400)
        if password is None or password == '':
            raise Error(message = 'password is required.', status_code=400)
        
        
        try:
            new_user = User(username=username, password=password, email=email, role=role, joined_at = datetime.now())
            db.session.add(new_user)
            db.session.commit()
            return new_user, 201
        except:
            raise Error(message="Cannot create User", status_code=409)    

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

    @marshal_with(user_fields) 
    def put(self, user_id): 
        args = message_parser.parse_args()
        username=args['username']
        
        if username is None or username == '':
            raise Error(message = 'username is required.', status_code=400)
        
        try:
            user = User.query.filter_by(user_id=user_id).one()
        except:
            raise Error(message="Internal Server Error", status_code=500)
       
        if user is None:
            raise Error(message="User not found", status_code=404)
        
        try:
            user.username = username
            db.session.commit()
            return user, 200
        except: 
            raise Error(message="User not updated", status_code=404)
        
    def delete(self, user_id):
        try:
            user = User.query.filter_by(user_id=user_id).one()
        except:
            raise Error(message="Internal Server Error", status_code=500)

        if user is None:
            raise Error(message="User not found", status_code=404)
        
        try:
            db.session.delete(user)
            db.session.commit()
            return "Successfully Deleted", 200
        except:
            raise Error(message="User Couldn\'t be deleted.", status_code=404)
        
