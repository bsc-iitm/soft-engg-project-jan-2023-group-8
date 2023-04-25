from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self):
        self.user_id = None
        self.username = None
        self.password = None
        self.display_name = None
        self.role = None
        self.faq = None
        
    def __init__(self, username, password, display_name, role, faq):
        self.username = username
        self.password = password
        self.display_name = display_name
        self.role = role
        self.faq = faq

    def register_user(self, username, password, role, display_name): 
        pass
    
    def login_user(self, username, password):
        pass
    
    def logout(self):
        pass
    
    @abstractmethod
    def display_tickets(self):
        pass
    
    def reply(self, ticket_id):
        pass
    
    def display_faq(self):
        pass
        
    