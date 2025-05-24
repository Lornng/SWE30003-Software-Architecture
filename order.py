import datetime

class Order:
    def __init__(self, order_id, customer, items):
        self.order_id = order_id
        self.customer = customer
        self.items = items.copy()
        self.total_price = sum(p.price * q for p, q in items.items())
        self.status = "Pending" # Order status (Pending, Shipped, Delivered, Cancelled)
        self.order_date = datetime.datetime.now()
