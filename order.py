from datetime import datetime

class Order:
    def __init__(self, order_id, customer, items, status, order_date, total_price=None, **kwargs):
        self.order_id = order_id
        self.customer = customer
        self.items = items
        self.status = status
        if isinstance(order_date, str):
            self.order_date = datetime.fromisoformat(order_date)
        else:
            self.order_date = order_date
        if total_price is not None:
            self.total_price = total_price
        else:
            self.total_price = sum(
                float(price) * int(qty) for price, qty in items.values()
            )

    def __str__(self):
        items_str = ', '.join([f"Product {pid}: {qty}" for pid, qty in self.items.items()])
        return (f"Order ID: {self.order_id}\n"
                f"Customer: {self.customer['name']} ({self.customer['email']})\n"
                f"Items: {items_str}\n"
                f"Total Price: ${self.total_price:.2f}\n"
                f"Status: {self.status}\n"
                f"Date: {self.order_date}")

