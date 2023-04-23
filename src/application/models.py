from application.db import db
from sqlalchemy.sql import func
from flask_login import UserMixin
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.Integer, nullable=False)
    joined_at = db.Column(db.DateTime(), default = datetime.utcnow, index = True)

    def get_id(self):
           return (self.user_id)
       
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)
      
    def __repr__(self):
        return f'<User {self.username}>'
    
class Ticket(db.Model):
    __tablename__ = 'Ticket'
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    likes = db.Column(db.Integer, nullable=False, default=0)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_resolved = db.Column(db.String, nullable=False, default="N")
    subject = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    
    def __repr__(self):
        return f'<Ticket {self.ticket_id}>'

class Message(db.Model):
    __tablename__ = 'Message'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    created_date =  db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    content = db.Column(db.String, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey(Ticket.ticket_id))

    def __repr__(self):
        return f'<Message {self.message_id}>'
    
class Notification(db.Model):
    __tablename__ = 'Notification'
    notify_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey(Ticket.ticket_id))
    message = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    created_date =  db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f'<Notification {self.notify_id}>'

class Faq(db.Model):
    __tablename__ = 'Faq'
    ticket_id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    
    def __repr__(self):
        return f'<FAQ {self.ticket_id}>'
    
    
class ResolvedUser(db.Model):
    __tablename__ = 'ResolvedUser'
    ticket_id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    
    def __repr__(self):
        return f'<Resolved User {self.ticket_id} {self.user_id}>'