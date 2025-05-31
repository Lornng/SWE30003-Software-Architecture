from datetime import datetime, timedelta
import random

class Delivery:
    SHIPPING_METHODS = ["Standard", "Express", "Overnight"]
    
    def __init__(self, delivery_id, address, method, order_id=None, 
                 status="Processing", tracking_number=None, estimated_delivery=None):
        self.delivery_id = delivery_id
        self.order_id = order_id
        self.address = address
        self.method = method if method in self.SHIPPING_METHODS else "Standard"
        self.status = status
        self.tracking_number = tracking_number or self._generate_tracking_number()
        
        # Error Fix: Handle estimated_delivery conversion
        if estimated_delivery is None:
            self.estimated_delivery = self.calculate_estimated_delivery()
        elif isinstance(estimated_delivery, str):
            try:
                self.estimated_delivery = datetime.fromisoformat(estimated_delivery)
            except (ValueError, TypeError):
                self.estimated_delivery = self.calculate_estimated_delivery()
        elif isinstance(estimated_delivery, datetime):
            self.estimated_delivery = estimated_delivery
        else:
            self.estimated_delivery = self.calculate_estimated_delivery()
    
    def _generate_tracking_number(self):
        """Generate a random 12-digit tracking number"""
        return f"TN{random.randint(100000000000, 999999999999):012d}"
    
    def calculate_estimated_delivery(self):
        """Calculate delivery date based on shipping method"""
        base_days = {
            "Standard": 5,
            "Express": 3,
            "Overnight": 1
        }
        days = base_days.get(self.method, 5)
        return datetime.now() + timedelta(days=days)
    
    def update_status(self, new_status):
        """Update delivery status with validation"""
        valid_statuses = ["Processing", "Shipped", "In Transit", 
                          "Out for Delivery", "Delivered", "Delayed"]
        if new_status in valid_statuses:
            self.status = new_status
            return True
        raise ValueError(f"Invalid status. Valid options: {', '.join(valid_statuses)}")
    
    def __str__(self):
        return (f"Delivery ID: {self.delivery_id}\n"
                f"Order ID: {self.order_id or 'N/A'}\n"
                f"Method: {self.method}\n"
                f"Address: {self.address}\n"
                f"Status: {self.status}\n"
                f"Tracking: {self.tracking_number}\n"
                f"Est. Delivery: {self.estimated_delivery.strftime('%Y-%m-%d')}")