from user import User

class Customer(User):
    def __init__(self, user_id, name, email, password, address, **kwargs):
        super().__init__(user_id, name, email, password)
        self.address = address
        self.orders = kwargs.get('orders', [])  
        
        # Handle any other extra fields from JSON gracefully
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)
    
    def update_address(self, address):
        self.address = address