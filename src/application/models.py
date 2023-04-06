from application.db import db

class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    display_name = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    
class Ticket(db.Model):
    __tablename__ = 'Ticket'
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    likes = db.Column(db.Integer, nullable=False, default=0)
    created_date = db.Column(db.DateTime, nullable=False)
    is_resolved = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    catagory = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

class Message(db.Model):
    __tablename__ = 'Message'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    created_date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey(Ticket.ticket_id))

class Notification(db.Model):
    __tablename__ = 'Notification'
    notify_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey(Ticket.ticket_id))
    message = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

class Faq(db.Model):
    __tablename__ = 'Faq'
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))