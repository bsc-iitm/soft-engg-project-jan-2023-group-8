from flask import make_response
from flask_restful import HTTPException

class Error(HTTPException):
    def __init__(self, message, status_code):
        self.response = make_response(message, status_code)
