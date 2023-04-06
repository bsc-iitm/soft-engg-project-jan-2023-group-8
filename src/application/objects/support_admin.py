from user import User

class SupportAdmin(User):
    def __init__(self, my_moved_tickets):
        self.my_moved_tickets = my_moved_tickets
        
    def display_tickets(self):
        pass
    
    def move_to_faq(ticket_id):
        pass
    
    def remove_from_faq(ticket_id):
        pass
    