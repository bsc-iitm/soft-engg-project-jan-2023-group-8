class Notification():
    def __init__(self):
        self.notify_id = None
        self.ticket_id = None
        self.message = None
        self.user_id = None
        
    def __init__(self, notify_id, ticket_id, message, user_id):
        self.notify_id = notify_id
        self.ticket_id = ticket_id
        self.message = message
        self.user_id = user_id

    def create(self, user_id, ticket_id, message): 
        pass
    
    def delete(self, notify_id):
        pass
        