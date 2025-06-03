from datetime import datetime
from payment import Payment
from delivery import Delivery

class Order:
    def __init__(self, order_id, customer, items, status, order_date, 
                 total_price=None, payment=None, delivery=None, **kwargs):
        self.order_id = order_id
        self.customer = customer
        self.items = items
        self.status = status
        
        # Handle order date 
        if isinstance(order_date, str):
            self.order_date = datetime.fromisoformat(order_date)
        else:
            self.order_date = order_date
        
        # Set total price
        self.total_price = total_price if total_price is not None else 0.0
        
        # Handle payment data
        # Error fix - Put "none" to ensure all required fields are present
        self.payment = None
        if payment:
            # Add missing order_id to payment data
            if isinstance(payment, dict):
                payment.setdefault('order_id', order_id)
                self.payment = Payment(**payment)
            elif isinstance(payment, Payment):
                self.payment = payment
        
        # Handle delivery data
        # Error fix - Put "none" to ensure all required fields are present
        self.delivery = None
        if delivery:
            # Add missing order_id to delivery data
            if isinstance(delivery, dict):
                delivery.setdefault('order_id', order_id)
                self.delivery = Delivery(**delivery)
            elif isinstance(delivery, Delivery):
                self.delivery = delivery
        
        # Handle additional fields
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        items_str = self.format_items()
        customer_info = self.format_customer_info()
        payment_info = self.format_payment_info()
        delivery_info = self.format_delivery_info()
        
        return (f"Order ID: {self.order_id}\n"
                f"{customer_info}"
                f"Items: {items_str}\n"
                f"Total Price: ${self.total_price:.2f}\n"
                f"Status: {self.status}\n"
                f"Date: {self.order_date}\n"
                f"{payment_info}"
                f"{delivery_info}")

    def format_items(self):
        """Format items based on storage type (list of dicts)"""
        if isinstance(self.items, list):
            return ', '.join([f"{item['product_id']} x {item['quantity']}" 
                             for item in self.items])
        return "No items"

    def format_customer_info(self):
        """Format customer information from dictionary"""
        if isinstance(self.customer, dict):
            return f"Customer: {self.customer.get('name', 'Unknown')} ({self.customer.get('email', 'No email')})\n"
        return "Customer: Information not available\n"

    def format_payment_info(self):
        """Format payment information if available"""
        if self.payment:
            return (f"Payment: {self.payment.method} ({self.payment.status})\n"
                    f"Payment ID: {self.payment.payment_id}\n")
        return "Payment: Not processed\n"

    def format_delivery_info(self):
        """Format delivery information if available"""
        if self.delivery:
            # Handle estimated_delivery date formatting
            est_delivery = self.delivery.estimated_delivery
            if isinstance(est_delivery, str):
                est_delivery = datetime.fromisoformat(est_delivery)
            
            return (f"Delivery: {self.delivery.method} ({self.delivery.status})\n"
                    f"Tracking: {self.delivery.tracking_number}\n"
                    f"Est. Delivery: {est_delivery.strftime('%Y-%m-%d')}\n")
        return "Delivery: Not scheduled\n"

    def update_status(self, new_status):
        """Update order status with validation"""
        valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled", "Refunded", "Pending Refund", "Refund Pending"]
        if new_status in valid_statuses:
            self.status = new_status
            return True
        print(f"Invalid status. Valid options: {', '.join(valid_statuses)}")
        return False