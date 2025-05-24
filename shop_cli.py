from shop import Shop
from cart import Cart

class ShopCLI:
    def __init__(self, shop):
        self.shop = shop
        self.current_customer = None
        self.cart = Cart()

    def run(self):
        # Registration/Login loop
        # Main menu: browse/search, view cart, view orders, logout
        pass
