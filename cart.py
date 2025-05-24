class Cart:
    def __init__(self):
        self.items = {}  # Product: quantity

    def add_product(self, product, quantity):
        self.items[product] = self.items.get(product, 0) + quantity

    def remove_product(self, product):
        if product in self.items:
            del self.items[product]

    def update_quantity(self, product, quantity):
        if product in self.items:
            self.items[product] = quantity

    def clear(self):
        self.items.clear()
