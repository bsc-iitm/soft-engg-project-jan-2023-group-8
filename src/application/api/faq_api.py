from application.api.api_init import *
from flask_restful import Resource, fields, marshal_with, reqparse
from application.models import Faq
from application.db import db
from datetime import datetime

faq_fields = {
    'user_id': fields.Integer, 
    'ticket_id': fields.Integer
}

message_parser = reqparse.RequestParser()
message_parser.add_argument('user_id')
message_parser.add_argument('ticket_id')

class FaqListAPI(Resource):
        
    @marshal_with(faq_fields)
    def get(self):
        try:
            faqs = Faq.query.all()
            return faqs, 200
        except:
            raise Error(message="Internal Server Error", status_code=500)
    
    @marshal_with(faq_fields) 
    def post(self): 
        args = message_parser.parse_args()
        ticket_id = args['ticket_id']
        user_id = args['user_id']

        # Argument Handling
        if ticket_id is None or ticket_id == '':
            raise Error(message = 'Ticket ID is required.', status_code=400)
        if ticket_id is None or ticket_id == '':
            raise Error(message = 'User ID is required.', status_code=400)
        
        try:
            new_faq = Faq(user_id=user_id, ticket_id=ticket_id)
            db.session.add(new_faq)
            db.session.commit()
            return new_faq, 201
        except:
            raise Error(message="Cannot add ticket to FAQ", status_code=409)

class FaqAPI(Resource):
    @marshal_with(faq_fields)
    def get(self, ticket_id):
        try:
            faq = Faq.query.filter_by(ticket_id=ticket_id).one()
        except:
            raise Error(message="Internal Server Error", status_code=500)
        if faq is None:
            raise Error(message ="Ticket not found in FAQ", status_code=404) 
        else:
            return faq, 200
        
    def delete(self, ticket_id):
        try:
            faq = Faq.query.filter_by(ticket_id=ticket_id).one()
        except:
            raise Error(message="Internal Server Error", status_code=500)

        if faq is None:
            raise Error(message="Ticket not found in faq", status_code=404)
        
        try:
            db.session.delete(faq)
            db.session.commit()
            return "Successfully Deleted", 200
        except:
            raise Error(message="Ticket in FAQ Couldn\'t be deleted.", status_code=404)
        
        
class FaqUserListAPI(Resource):
    @marshal_with(faq_fields)
    def get(self, user_id):
        try:
            faq = Faq.query.filter_by(user_id=user_id).all()
        except:
            raise Error(message="Internal Server Error", status_code=500)
        if faq is None:
            raise Error(message ="Ticket not found in FAQ", status_code=404) 
        else:
            return faq, 200


