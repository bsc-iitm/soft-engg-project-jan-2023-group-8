from application.api.api_init import *
from flask_restful import Resource, fields, marshal_with,reqparse
from application.models import Ticket
from application.db import db
from datetime import datetime


ticket_fields = {
    'user_id': fields.Integer,
    'ticket_id': fields.Integer, 
    'likes': fields.Integer,
    'subject': fields.String,
    'category': fields.String,
    'created_date': fields.DateTime,
    'is_resolved': fields.String
}

message_parser = reqparse.RequestParser()
message_parser.add_argument('user_id')
message_parser.add_argument('likes')
message_parser.add_argument('subject')
message_parser.add_argument('category')
message_parser.add_argument('is_resolved')


class TicketListAPI(Resource):
        
    @marshal_with(ticket_fields)
    def get(self, user_id):
        try:
            ticket = Ticket.query.filter_by(user_id=user_id).all()
        except:
            raise Error(message="Internal Server Error", status_code=500)
        if ticket is None:
            raise Error(message ="ticket not found", status_code=404) 
        else:
            return ticket, 200
       
    @marshal_with(ticket_fields) 
    def post(self, user_id): 
        args = message_parser.parse_args()
        subject = args['subject']
        category=args['category']
        is_resolved = args['is_resolved']
        likes = args['likes']
                
        # Argument Handling
        if subject is None or subject == '':
            raise Error(message = 'subject is required.', status_code=400)
        if user_id is None or user_id == '':
            raise Error(message = 'user id is required.', status_code=400)
        if category is None or category == '':
            raise Error(message = 'category is required.', status_code=400)
        
        
        try:
            new_ticket = Ticket(user_id=user_id, subject=subject, category=category, likes=likes, is_resolved = is_resolved,created_date = datetime.now())
            db.session.add(new_ticket)
            db.session.commit()
            return new_ticket, 201
        except:
            raise Error(message="Cannot create Ticket", status_code=409)    

class TicketAPI(Resource):
    @marshal_with(ticket_fields)
    def get(self, user_id, ticket_id):
        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).one()
        except:
            raise Error(message="Internal Server Error", status_code=500)
        if ticket is None:
            raise Error(message ="ticket not found", status_code=404) 
        else:
            return ticket, 200
        
    @marshal_with(ticket_fields) 
    def put(self, user_id, ticket_id): 
        args = message_parser.parse_args()
        subject = args['subject']
        category=args['category']
        
        try:
            if subject is None or subject == '':
                raise Error(message = 'subject is required.', status_code=400)
            if category is None or category == '':
                raise Error(message = 'category is required.', status_code=400)        
            
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).one()
            
            if ticket is None:
                raise Error(message="Ticket not found", status_code=404)       
            try:
                ticket.subject = subject
                ticket.category=category
                db.session.commit()
                return ticket, 200
            except: 
                raise Error(message="Ticket not updated", status_code=404)
        except:
            raise Error(message="Internal Server Error", status_code=500)
       

    
    def delete(self, user_id, ticket_id):

        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).one()
        except:
            raise Error(message="Internal Server Error", status_code=500)

        if ticket is None:
            raise Error(message="Ticket not found", status_code=404)
        
        try:
            db.session.delete(ticket)
            db.session.commit()
            return "Successfully Deleted", 200
        except:
            raise Error(message="Ticket Couldn\'t be deleted.", status_code=404)
        
