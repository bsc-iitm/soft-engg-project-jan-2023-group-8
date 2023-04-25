from user import User

class SupportStaff(User):
    def __init__(self, handled_tickets):
        self.handled_tickets = handled_tickets
        
    def display_tickets(self):
        pass
    
    def mark_resolved(self, ticket_id):
        pass
    
    def mark_unresolved(self, ticket_id):
        pass
    