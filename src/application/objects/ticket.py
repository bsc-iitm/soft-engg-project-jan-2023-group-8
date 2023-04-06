class Ticket():
    def __init__(self):
        self.ticket_id = None
        self.likes = None
        self.created_date = None
        self.is_resolved = None
        self.subject = None
        self.messages = None
        self.user_id = None
        
    def __init__(self, likes, created_date, is_resolved, subject, messages, user_id):
        self.likes = likes
        self.created_date = created_date
        self.is_resolved = is_resolved
        self.subject = subject
        self.messages = messages
        self.user_id = user_id
        
    def incr_likes(self):
        pass
    
    def decr_likes(self):
        pass
    
    def set_resolved(self, is_resolved):
        pass
    
    def reply(self, ticket_id, user_id):
        pass
    