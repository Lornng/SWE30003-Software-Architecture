from datetime import datetime

class Order:
    def __init__(self, order_id, customer, items, total_price, status, order_date, **kwargs):
        self.order_id = order_id
        self.customer = customer
        self.items = items
        self.total_price = total_price
        self.status = status
        if isinstance(order_date, str):
            self.order_date = datetime.fromisoformat(order_date)
        else:
            self.order_date = order_date

    def __str__(self):
        items_str = ', '.join(
            [f"{item['product_id']}: {item['quantity']}" for item in self.items]
        )
        customer_name = self.customer.get('name', self.customer)
        return (f"Order ID: {self.order_id}\n"
                f"Customer: {customer_name}\n"
                f"Items: {items_str}\n"
                f"Total Price: ${self.total_price:.2f}\n"
                f"Status: {self.status}\n"
                f"Date: {self.order_date}")



