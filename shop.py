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

    # Methods for product, customer, order, and admin management
