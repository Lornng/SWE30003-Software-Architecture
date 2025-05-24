from user import User

class Customer(User):
    def __init__(self, user_id, name, email, password, address):
        super().__init__(user_id, name, email, password)
        self.address = address
        self.order_history = []