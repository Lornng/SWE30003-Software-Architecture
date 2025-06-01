class Cart:
    def __init__(self):
        self.items = {}  # Product: quantity

    def add_product(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        existing_quantity = self.items.get(product, 0)
        total_quantity = existing_quantity + quantity
        
        if total_quantity > product.stock:
            raise ValueError(f"Insufficient stock. Available: {product.stock - existing_quantity}")
        
        self.items[product] = total_quantity
        return True

    def remove_product(self, product):
        if product in self.items:
            del self.items[product]

    def update_quantity(self, product, quantity):
        if product not in self.items:
            raise ValueError("Product not in cart")
        
        if quantity == 0:
            return self.remove_product(product)
        
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        if quantity > product.stock:
            raise ValueError(f"Insufficient stock. Available: {product.stock}")
        
        self.items[product] = quantity
        return True

    def clear(self):
        self.items.clear()
        
    def get_total_price(self):
        return sum(product.price * quantity for product, quantity in self.items.items())
    
    def get_total_items(self):
        """Get total number of items in cart"""
        return sum(self.items.values())
    
    def is_empty(self):
        return len(self.items) == 0
    
    def get_subtotal(self, product):
        if product in self.items:
            return product.price * self.items[product]
        return 0
    
    def validate_stock_availability(self):
        unavailable_items = []
        for product, quantity in self.items.items():
            if not product.is_in_stock(quantity):
                unavailable_items.append({
                    'product': product,
                    'requested': quantity,
                    'available': product.stock
                })
        return unavailable_items
    
    def get_cart_summary(self):
        if self.is_empty():
            return "Cart is empty"
        
        summary = []
        for product, quantity in self.items.items():
            subtotal = self.get_subtotal(product)
            summary.append({
                'name': product.name,
                'quantity': quantity,
                'price': product.price,
                'subtotal': subtotal
            })
        
        return {
            'items': summary,
            'total': self.get_total_price(),
            'item_count': self.get_total_items()
        }

