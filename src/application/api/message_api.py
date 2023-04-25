from application.api.api_init import *
from flask_restful import Resource, fields, marshal_with, reqparse
from application.models import Message
from application.db import db
from datetime import datetime

message_fields = {
    'message_id': fields.Integer,
    'user_id': fields.Integer, 
    'created_date': fields.DateTime,
    'content': fields.String,
    'ticket_id': fields.Integer
}

message_parser = reqparse.RequestParser()
message_parser.add_argument('user_id')
message_parser.add_argument('content')
message_parser.add_argument('ticket_id')

class MessageListAPI(Resource):
        
    @marshal_with(message_fields)
    def get(self, ticket_id):
        try:
            messages = Message.query.filter_by(ticket_id=ticket_id).all()
            return messages, 200
        except:
            raise Error(message="Internal Server Error", status_code=500)
    
    @marshal_with(message_fields) 
    def post(self, ticket_id): 
        args = message_parser.parse_args()
        content = args['content']
        user_id = args['user_id']

        # Argument Handling
        if content is None or content == '':
            raise Error(message = 'Message Content is required.', status_code=400)
        if ticket_id is None or ticket_id == '':
            raise Error(message = 'User ID is required.', status_code=400)
        
        try:
            new_message = Message(user_id=user_id, content=content, ticket_id=ticket_id, created_date = datetime.now())
            db.session.add(new_message)
            db.session.commit()
            return new_message, 201
        except:
            raise Error(message="Cannot create message", status_code=409)

class MessageAPI(Resource):
    @marshal_with(message_fields)
    def get(self, ticket_id, message_id):
        try:
            message = Message.query.filter_by(message_id=message_id).one()
        except:
            raise Error(message="Internal Server Error", status_code=500)
        if message is None:
            raise Error(message ="Message not found", status_code=404) 
        else:
            return message, 200
        
    @marshal_with(message_fields)
    def put(self, ticket_id, message_id):
        args = message_parser.parse_args()
        content = args['content']

        # Argument Handling
        if content is None or content == '':
            raise Error(message = 'Content is required / shouldn\'t be empty', status_code=400)
        try:
            message = Message.query.filter_by(message_id=message_id).one()
        except:
            raise Error(message="Internal Server Error", status_code=500)
       
        if message is None:
            raise Error(message="Message not found", status_code=404)
        
        try:
            message.content = content
            db.session.commit()
            return message, 200
        except: 
            raise Error(message="Message not updated", status_code=404)
        
    def delete(self, ticket_id, message_id):
        try:
            message = Message.query.filter_by(message_id=message_id).one()
        except:
            raise Error(message="Internal Server Error", status_code=500)

        if message is None:
            raise Error(message="Message not found", status_code=404)
        
        try:
            db.session.delete(message)
            db.session.commit()
            return "Successfully Deleted", 200
        except:
            raise Error(message="Message Couldn\'t be deleted.", status_code=404)
        
