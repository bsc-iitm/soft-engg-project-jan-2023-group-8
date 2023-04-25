class Message():
    def __init__(self):
        self.message_id = None
        self.user_id = None
        self.created_date = None
        self.content = None
        self.ticket_id = None
        
    def __init__(self, user_id, created_date, content, ticket_id):
        self.user_id = user_id
        self.created_date = created_date
        self.content = content
        self.ticket_id = ticket_id

    def create_msg(self, ticket_id, message_id, content): 
        pass
    
    def edit_msg(self, message_id, content):
        pass
    
    def delete_msg(self, message_id):
        pass

        