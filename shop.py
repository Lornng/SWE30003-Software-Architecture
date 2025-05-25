import json
import os
from product import Product
from customer import Customer
from admin import Admin
from order import Order


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
            if product.product_id == product_id:
                return product
        return None

    def list_products(self):
        return self.products

    def search_products(self, keyword):
        return [p for p in self.products if keyword.lower() in p.name.lower() or keyword.lower() in p.description.lower()]

    def list_products_by_category(self, category):
        return [p for p in self.products if p.category.lower() == category.lower()]

    # ---------- Customer Management ----------
    def register_customer(self, customer):
        self.customers.append(customer)

    def find_customer_by_email(self, email):
        for customer in self.customers:
            if customer.email == email:
                return customer
        return None

    def list_customers(self):
        return self.customers

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
    def place_order(self, customer, cart):
        for product, qty in cart.items.items():
            if not product.is_in_stock(qty):
                return None
        for product, qty in cart.items.items():
            product.update_stock(qty)
        order = Order(len(self.orders) + 1, customer, cart.items)
        self.orders.append(order)
        customer.add_order(order)
        cart.clear()
        return order

    def list_orders(self):
        return self.orders

    def list_orders_by_customer(self, customer):
        return [order for order in self.orders if order.customer['user_id'] == customer.user_id]


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


    def save_data(self):
        # saving to JSON files for products, customers, admins, orders
        # products:
        with open("data/products.json", "w") as f:
            json.dump([vars(p) for p in self.products], f, indent=2)
        # Repeat for customers, admins, orders

