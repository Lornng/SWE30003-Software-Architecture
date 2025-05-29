class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
    
    def authenticate(self, email, password):
        return self.email == email and self.password == password
    
    def update_profile(self, name=None, email=None, password=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if password:
            self.password = password
            
            