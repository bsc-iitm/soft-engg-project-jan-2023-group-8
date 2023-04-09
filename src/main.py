import os
from flask import Flask
from flask_restful import Api
from application.db import db, db_dir
from application.api.user_api import UserAPI, UserListAPI
from application.api.message_api import MessageAPI, MessageListAPI

# ----------------- Configurations --------------------------------

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///" + os.path.abspath(db_dir)
app.config['SECRET_KEY'] = 'dce10f96e430dfc3395fa456fcbaf105456b6cb950953a873067477f17eaf54e'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = "bcrypt"
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['timezone'] = 'Asia/Kolkata'

db.init_app(app)

api.add_resource(UserAPI, '/api/user/<int:user_id>')
api.add_resource(UserListAPI, '/api/user')
api.add_resource(MessageListAPI, '/api/ticket/<int:ticket_id>/message')
api.add_resource(MessageAPI, '/api/ticket/<int:ticket_id>/message/<int:message_id>')

if __name__ == '__main__':
    app.run(host='localhost', port='8080', debug=True)