from datetime import datetime
import random

class Payment:
    
    VALID_METHODS = ["Credit Card", "PayPal", "Bank Transfer", "Cash on Delivery"]

    def __init__(self, payment_id,amount, method, order_id=None, status="Pending", transaction_date=None):
        self.payment_id = payment_id
        self.order_id = order_id #optional to be none
        self.amount = amount
        self.method = method if method in self.VALID_METHODS else "Credit Card"
        self.status = status
        # Robust transaction_date handling with error prevention
        if transaction_date is None:
            self.transaction_date = datetime.now()
        elif isinstance(transaction_date, str):
            try:
                self.transaction_date = datetime.fromisoformat(transaction_date)
            except (ValueError, TypeError):
                # Fallback to current time if format is invalid
                self.transaction_date = datetime.now()
                print(f"Warning: Invalid date format for payment {payment_id}. Using current time.")
        elif isinstance(transaction_date, datetime):
            self.transaction_date = transaction_date
        else:
            # Handle unexpected types
            self.transaction_date = datetime.now()
            print(f"Warning: Unexpected date type for payment {payment_id}. Using current time.")
    
    def process_payment(self):
        # """Simulate payment processing"""
        success_rates = {
            "Credit Card": 0.95,
            "PayPal": 0.90,
            "Bank Transfer": 0.85,
            "Cash on Delivery": 1.0  # Always succeeds
        }
        #Use this to create different instance of success for fail
        success = random.random() < success_rates.get(self.method, 0.9) 
        self.status = "Completed" if success else "Failed"
        self.transaction_date = datetime.now()
        return success

    def __str__(self):
        return (f"Payment ID: {self.payment_id}\n"
                f"Order ID: {self.order_id or 'N/A'}\n"
                f"Method: {self.method}\n"
                f"Amount: ${self.amount:.2f}\n"
                f"Status: {self.status}\n"
                f"Date: {self.transaction_date}")