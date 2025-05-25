class Product:
    def __init__(self, product_id, name, description, price, stock, category):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category = category

    def __str__(self):
        return (f"[{self.product_id}] {self.name} ({self.category})\n"
                f"  Description: {self.description}\n"
                f"  Price: ${self.price:.2f} | Stock: {self.stock}")
