import json
import os
import re
from product import Product
from customer import Customer
from admin import Admin
from order import Order
from delivery import Delivery
from datetime import datetime
from payment import Payment

class Shop:
    def __init__(self):
        self.products = []
        self.customers = []
        self.orders = []
        self.admins = []
            
    # ---------- Product Management ----------
    def add_product(self, product):
        self.products.append(product)

    def modify_product(self, product_id, **kwargs):
        product = self.find_product_by_id(product_id)
        if product:
            for key, value in kwargs.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            return True
        return False

    def delete_product(self, product_id):
        product = self.find_product_by_id(product_id)
        if product:
            self.products.remove(product)
            return True
        return False

    def find_product_by_id(self, product_id):
        for product in self.products:
            if str(product.product_id).lower() == str(product_id).lower():
                return product
        return None


    def list_products(self):
        return self.products

    def search_products(self, keyword):
        return [p for p in self.products if keyword.lower() in p.name.lower() or keyword.lower() in p.description.lower()]

    def list_products_by_category(self, category):
        return [p for p in self.products if p.category.lower() == category.lower()]
    
    def get_product_categories(self):
        return list(set(p.category for p in self.products))

    # ---------- Customer Management ----------
    def validate_name(self, name):
        name_pattern = r"^[A-Za-z\s'-]+$"
        if not re.match(name_pattern, name):
            return False, "Full Name can only contain letters, spaces, hyphens(-), or apostrophes(')."
        
        return True, ""
    
    def validate_email_for_register(self, email):
        # Check format
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            return False, "Invalid email format. Please try again."
        
        # Check if already exists
        if self.find_customer_by_email(email):
            return False, "Email already taken. Please try a different email."
        
        return True, ""
    
    def validate_email_for_update(self, email, current_user_id):
        # Check format
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            return False, "Invalid email format. Please try again."
        
        # Check if taken by another customer
        existing_customer = self.find_customer_by_email(email)
        if existing_customer and existing_customer.user_id != current_user_id:
            return False, "Email already taken by another customer. Try again or leave blank to keep current."
        
        return True, ""
    
    def validate_password(self, password):      
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        
        return True, ""
    
    def existing_customer_email(self, email, current_user_id):
        existing_customer = self.find_customer_by_email(email)
        return existing_customer and existing_customer.user_id != current_user_id

    
    def register_customer(self, customer_data):
        name, email, password, address = customer_data
        
        # Generate customer IDs
        user_id = f"U{len(self.customers) + 1:03d}" 
        
        # Create and add customer
        new_customer = Customer(user_id, name.strip(), email.strip(), password, address.strip())
        self.customers.append(new_customer)
        return True, "Customer registered successfully."
    
    def authenticate_customer(self, email, password):
        customer = self.find_customer_by_email(email)
        if customer and customer.password == password:
            return customer
        return None

    def find_customer_by_email(self, email):
        email = email.lower()
        for customer in self.customers:
            if customer.email.lower() == email:
                return customer
        return None

    def list_customers(self):
        return self.customers
    
    def update_customer_profile(self, customer, profile_data):
        try:
            if profile_data['name'] is not None:
                customer.name = profile_data['name']
            if profile_data['email'] is not None:
                customer.email = profile_data['email']
            if profile_data['password'] is not None:
                customer.password = profile_data['password']
            if profile_data['address'] is not None:
                customer.address = profile_data['address']
            return True, "Profile updated successfully"
        except Exception as e:
            return False, str(e)

    # ---------- Admin Management ----------
    def add_admin(self, admin):
        self.admins.append(admin)

    def find_admin_by_email(self, email):
        for admin in self.admins:
            if admin.email.strip().lower() == email.strip().lower():
                return admin
        return None

    def list_admins(self):
        return self.admins

    # ---------- Order Management ----------

    def list_orders(self):
        return self.orders

    def list_orders_by_customer(self, customer):
            return [
        order for order in self.orders
        if str(order.customer['user_id']).lower() == str(customer.user_id).lower()
    ]

    # ---------------Create an order from the cart contents------------------
    def place_order(self, customer, cart, payment_method):
        # First check stock for all items in cart
        for product, quantity in cart.items.items():
            if product.stock < quantity:
                print(f"Error:Insufficient stock for {product.name}")
                print(f"Request: {quantity}, Available {product.stock}")
                return None

        # Convert cart items to the format we need for orders
        items_list = []
        for product, quantity in cart.items.items():
            items_list.append({
                "product_id": product.product_id,
                "quantity": quantity
            })
        
        # Generate order IDs
        order_id = f"ORD{len(self.orders) + 1:04d}"
        # payment_id = f"PAY{len(self.orders) + 1:04d}"
        # delivery_id = f"DLV{len(self.orders) + 1:04d}"
        payment_id = f"DLV{order_id[3:]}"
        delivery_id = f"DLV{order_id[3:]}"
        total_price=sum(product.price * qty for product, qty in cart.items.items())
        
        # Create order
        order = Order(
            order_id=order_id,
            customer=vars(customer),  # Convert customer object to dict
            items=items_list,
            status="Pending",
            order_date=datetime.now(),
            total_price=total_price
        )
        
        # Create payment
        payment = Payment(
            payment_id=payment_id,
            order_id=order_id,
            amount=total_price,
            method=payment_method,
            transaction_date=datetime.now(),
        )
        
        # Process payment (simulated)
        if payment.process_payment():
            order.status = "Confirmed 💸"
            # Update stock
            for product, quantity in cart.items.items():
                product.stock -= quantity
        else:
            order.status = "Payment Failed ⛔"
        
        # Create delivery
        delivery = Delivery(
            delivery_id=delivery_id,
            order_id=order_id,
            address=customer.address,
            method="Standard",
            estimated_delivery=None
        )
        
        # Associate payment and delivery with order
        order.payment = payment
        order.delivery = delivery
        
        # Save the order
        self.orders.append(order)
        
        # Also add to customer's orders
        customer.orders.append(order.order_id)  # Store just the order ID
        
        # Clear the cart
        cart.clear()
        
        return order
    
    # ---------- Load/Save Data ----------
    def load_data(self):
        def load_json_file(filename):
            if not os.path.exists(filename):
                return []
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                    return data
                except json.JSONDecodeError:
                    return []
        
        products_data = load_json_file("data/products.json")
        self.products = [Product(**prod) for prod in products_data]

        customers_data = load_json_file("data/customers.json")
        self.customers = [Customer(**cust) for cust in customers_data]

        admins_data = load_json_file("data/admins.json")
        self.admins = [Admin(**adm) for adm in admins_data]

        orders_data = load_json_file("data/orders.json")
        self.orders = [Order(**ordr) for ordr in orders_data]

    # def save_data(self):
    #     # saving to JSON files for products, customers, admins, orders
    #     # products:
    #     with open("data/products.json", "w") as f:
    #         json.dump([vars(p) for p in self.products], f, indent=2)
    #     # Repeat for customers, admins, orders
        
    #     # Save customers
    #     with open("data/customers.json", "w") as f:
    #         json.dump([vars(c) for c in self.customers], f, indent=2)

    def save_data(self):
        # Save products
        with open("data/products.json", "w") as f:
            products_data = [{
                "product_id": p.product_id,
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "stock": p.stock,
                "category": p.category
            } for p in self.products]
            json.dump(products_data, f, indent=2)
        
        # Save customers
        with open("data/customers.json", "w") as f:
            customers_data = [{
                "user_id": c.user_id,
                "name": c.name,
                "email": c.email,
                "password": c.password,
                "address": c.address,
                "orders": c.orders
            } for c in self.customers]
            json.dump(customers_data, f, indent=2)
        
        # Save orders
        with open("data/orders.json", "w") as f:
                orders_data = []
                for order in self.orders:
                    # Convert Order object to JSON-serializable dict
                    order_dict = {
                        "order_id": order.order_id,
                        "customer": order.customer,
                        "items": order.items,
                        "status": order.status,
                        "order_date": self.safe_isoformat(order.order_date),
                        "total_price": order.total_price
                    }
                    
                    # Add payment data if exists
                    if hasattr(order, 'payment') and order.payment:
                        payment = order.payment
                        payment_dict = {
                            "payment_id": payment.payment_id,
                            "order_id": payment.order_id,
                            "amount": payment.amount,
                            "method": payment.method,
                            "status": payment.status,
                            "transaction_date": self.safe_isoformat(payment.transaction_date)
                        }
                        order_dict["payment"] = payment_dict
                    
                    # Add delivery data if exists
                    if hasattr(order, 'delivery') and order.delivery:
                        delivery = order.delivery
                        delivery_dict = {
                            "delivery_id": delivery.delivery_id,
                            "order_id": delivery.order_id,
                            "address": delivery.address,
                            "method": delivery.method,
                            "status": delivery.status,
                            "tracking_number": delivery.tracking_number,
                            "estimated_delivery": self.safe_isoformat(delivery.estimated_delivery)
                        }
                        order_dict["delivery"] = delivery_dict
                    
                    orders_data.append(order_dict)
                
                json.dump(orders_data, f, indent=2)
        
        # Save admins
        with open("data/admins.json", "w") as f:
            admins_data = [{
                "user_id": a.user_id,
                "name": a.name,
                "email": a.email,
                "password": a.password
            } for a in self.admins]
            json.dump(admins_data, f, indent=2)

    def safe_isoformat(self, date_value):
        #Convert datetime to ISO string, handling strings and None
        if isinstance(date_value, datetime):
            return date_value.isoformat()
        elif isinstance(date_value, str):
            # Already in string format, return as-is
            return date_value
        elif date_value is None:
            return None
        else:
            # Fallback for unexpected types
            return str(date_value)