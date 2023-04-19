import os
from flask import Flask
from flask_restful import Api
from application.db import db, db_dir
from application.api.user_api import UserAPI, UserListAPI
from application.api.ticket_api import TicketAPI, TicketListAPI
from application.api.message_api import MessageAPI, MessageListAPI
from application.api.faq_api import FaqAPI, FaqListAPI, FaqUserListAPI
from flask_login import LoginManager

# ----------------- Configurations --------------------------------

app = Flask(__name__)
login_manager = LoginManager()
api = Api(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///" + os.path.abspath(db_dir)
app.config['SECRET_KEY'] = 'dce10f96e430dfc3395fa456fcbaf105456b6cb950953a873067477f17eaf54e'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = "bcrypt"
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['timezone'] = 'Asia/Kolkata'

db.init_app(app)
login_manager.init_app(app)

api.add_resource(UserListAPI, '/api/user')
api.add_resource(UserAPI, '/api/user/<int:user_id>')
api.add_resource(TicketListAPI, '/api/user/<int:user_id>/ticket')
api.add_resource(TicketAPI, '/api/user/<int:user_id>/ticket/<int:ticket_id>')
api.add_resource(MessageListAPI, '/api/ticket/<int:ticket_id>/message')
api.add_resource(MessageAPI, '/api/ticket/<int:ticket_id>/message/<int:message_id>')
api.add_resource(FaqListAPI, '/api/faq')
api.add_resource(FaqAPI, '/api/faq/ticket/<int:ticket_id>')
api.add_resource(FaqUserListAPI, '/api/faq/user/<int:user_id>')

from application.controllers.app import *
from application.controllers.auth import *

if __name__ == '__main__':
    app.run(host='localhost', port='8080', debug=True)
