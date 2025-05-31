from cart import Cart
from customer import Customer
import re

class ShopCLI:
    def __init__(self, shop):
        self.shop = shop
        self.current_customer = None
        self.cart = Cart()

    def run(self):
        while True:
            if not self.current_customer:
                # Show login/register menu
                print("\n--- Customer Portal ---")
                print("1. Login")
                print("2. Register")
                print("3. Back to Main Menu")
                choice = input("Enter your choice: ").strip()
                
                if choice == "1":
                    self.login()
                elif choice == "2":
                    self.register()
                elif choice == "3":
                    break
                else:
                    print("\nInvalid choice. Please enter a number between 1 and 3.")
            else:
                # Show main customer menu
                self.customer_menu()
                

    def login(self):
        print("\n--- Customer Login ---")
        print("\nType 'exit' at any prompt to cancel login.")
         
        # Email prompt
        while True:
            email = input("\nEmail: ").strip()
            if email.lower() == 'exit':
                print("\nLogin cancelled.")
                return
            if not email:
                print("\nEmail is required.")
                continue
            break
        
        # Password prompt
        while True:
            password = input("\nPassword: ").strip()
            if password.lower() == 'exit':
                print("\nLogin cancelled.")
                return
            if not password:
                print("\nPassword is required.")
                continue
            break
        
        # Authenticate user
        customer = self.shop.find_customer_by_email(email)
        if customer and customer.password == password:
            self.current_customer = customer
            print(f"Welcome back, {customer.name}!")
        else:
            print("\nInvalid email or password. Please try again.")
            

    def register(self):
        print("\n--- Customer Registration ---")
        print("\nType 'exit' at any prompt to cancel registration.")
        try:
            # Full Name prompt and format validation
            while True:
                name = input("\nFull Name: ").strip()
                name_pattern = r"^[A-Za-z\s'-]+$"
                if name.lower() == 'exit':
                    print("\nRegistration cancelled.")
                    return
                if not name:
                    print("\nName is required.")
                    continue
                if not re.match(name_pattern, name):
                    print("\nFull Name can only contain letters, spaces, hyphens(-), or apostrophes(').")
                    continue
                break
            
            # Email prompt and format validation
            while True: 
                email = input("\nEmail: ").strip()
                email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
                if email.lower() == 'exit':
                    print("\nRegistration cancelled.")
                    return
                if not email:
                    print("\nEmail is required.")
                    continue
                # Email format validation
                elif not re.match(email_pattern, email):
                    print("\nInvalid email format. Please try again.")
                    continue
                break
            
            # Prompt for password and check minimum length
            while True:
                password = input("\nPassword: ").strip()
                if password.lower() == 'exit':
                    print("\nRegistration cancelled.")
                    return
                if not password:
                    print("\nPassword is required.")
                    continue
                elif len(password) < 6:
                    print("\nPassword must be at least 6 characters long.")
                    continue
                break
            
            # Address Prompt
            while True:
                address = input("\nAddress: ").strip()
                if address.lower() == 'exit':
                    print("\nRegistration cancelled.")
                    return
                if not address: 
                    print("\nAddress is required.")
                    continue
                break
                
            # Check if email already exists
            if self.shop.find_customer_by_email(email):
                print("Email already registered. Please use a different email.")
                return
            
            # Generate new user ID
            user_id = max([c.user_id for c in self.shop.customers], default=0) + 1
            
            # Create new customer
            new_customer = Customer(user_id, name, email, password, address)
            self.shop.register_customer(new_customer)
            
            print("Registration successful! You can now login.")
            
        except Exception as e:
            print(f"Registration failed: {e}")
            

    def customer_menu(self):
        while True:
            print(f"\n--- Welcome, {self.current_customer.name}! ---")
            print("1. Browse All Products")
            print("2. Search Products")
            print("3. Browse by Category")
            print("4. View Cart")
            print("5. Update Profile")
            print("6. View Order History")
            print("7. Request Refund")
            print("8. Logout")
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.browse_products()
            elif choice == "2":
                self.search_products()
            elif choice == "3":
                self.browse_by_category()
            elif choice == "4":
                self.view_cart()
            elif choice == "5":
                self.update_profile()
            elif choice == "6":
                self.view_order_history()
            elif choice == "7":
                self.request_refund()
            elif choice == "8":
                print("Logging out...")
                self.current_customer = None
                self.cart.clear()
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 8.")
                
                
    # Browse products
    def browse_products(self):
        print("\n--- All Electronic Products ---")
        products = self.shop.list_products()
        
        if not products:
            print("\nNo electronic products available")
            return
        
        for product in products:
            print(product)
            print("-" * 50)
            
        self.add_to_cart_prompt(products)
        
            
    # Search for products
    def search_products(self):
        print("\n--- Search Products ---")
        
        while True:
            term = input("Please enter search term: ").strip()
             
            if not term:
                print("Search term cannot be empty.\n")
                continue
            
            if term.lower() == "exit":
                print("\nSearch cancelled.")
                return
            
            products = self.shop.search_products(term)
            
            if not products:
                print("No products found matching your search.")
            else: 
                print(f"\nFound {len(products)} product(s):")
                for product in products:
                    print(product)
                    print("-" * 50)
                    
                self.add_to_cart_prompt(products)
                print("\n--- Search again or type 'exit' to leave ---\n")
                
                
    # Browse products by category
    def browse_by_category(self):
        print("\n--- Browse products by Category ---")
        
        # Get all categories
        categories = list(set(p.category for p in self.shop.products))
        
        if not categories:
            print("\nCategories not available.")
            return
        
        print("\nCategories List:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
            
        try:
            choice = int(input("\nPlease select a category number: ").strip())
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                products = self.shop.list_products_by_category(selected_category)
                
                if not products:
                    print(f"\nNo product found in {selected_category} category.")
                    return
                
                print(f"\n--- Products in {selected_category} ---")
                for i, product in enumerate(products, 1):
                    print(f"{i}. {product}")
                    print("-" * 50)
                    
                self.add_to_cart_prompt(products)
            else: 
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            
    
    def add_to_cart_prompt(self, allowed_products = None):
        while True:
            choice = input("\nWould you like to add a product to cart? (y/n): ").strip().lower()
            if choice == 'y':
                 while True:
                    self.add_multiple_products_to_cart(allowed_products)
                    break
            elif choice == 'n':
                break
            else:
                print("\nPlease enter 'y' or 'n'.")
                
                
    def add_multiple_products_to_cart(self, allowed_products):
        while True:
            self.add_to_cart(allowed_products)
            again = input("\nWould you like to add another product? (y/n): ").strip().lower()
            if again == 'y':
                continue
            elif again == 'n':
                break
            else:
                print("\nInvalid input. Returning to main menu.")
                break
            
    def add_to_cart(self, allowed_products = None):
        while True:
            try: 
                product_id_input = input("\nPlease enter Product ID to add to cart (or type 'exit' to cancel): ").strip()
                if product_id_input.lower() == 'exit':
                    print("\nAdd item to cart cancelled.")
                    return
                
                product_id = int(product_id_input)
                product = self.shop.find_product_by_id(product_id)
                
                if not product:
                    print("\nProduct not found. Please try again.")
                    continue
                
                if allowed_products and product not in allowed_products:
                    print("\nProduct not available in this view. Please select a valid product.")
                    continue
                
                while True:
                    quantity_input = input(f"\nEnter quantity for '{product.name}' (stock: {product.stock}) (or type 'exit' to cancel): ").strip()
                    
                    if quantity_input.lower() == 'exit':
                        print(f"\nAdd {product.name} to cart cancelled")
                        return
                    
                    try:
                        quantity = int(quantity_input)
                    except ValueError:
                        print("\nInvalid quantity. Please enter a valid number.")
                        continue
                        
                    if quantity <= 0:
                        print("\nQuantity must be greater than 0.")
                        continue
                        
                    if quantity > product.stock:
                        print(f"\nSorry, only {product.stock} items available in stock.")
                        continue
                    
                    existing_quantity = self.cart.items.get(product, 0)
                    total_quantity = existing_quantity + quantity
                        
                    if total_quantity > product.stock:
                        print(f"\nSorry, you already have {existing_quantity} in your cart.")
                        print(f"Adding {quantity} would exceed stock. Only {product.stock - existing_quantity} more available.")
                        continue
                        
                    self.cart.add_product(product, quantity)
                    print(f"\nAdded {product.name} x {quantity} to cart.")
                    return
                
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")
                
            
    """ 
    Displays the contents of the shopping cart and provides users with the option to update products quantity, 
    remove products, clear cart, proceed to checkout, or continue shopping.
    """
    def view_cart(self):

        while True:
            print("\n--- Your Shopping Cart ---")
            if not self.cart.items:
                print("Your cart is empty.")
                return
        
            total = 0
            for product, quantity in self.cart.items.items():
                subtotal = product.price * quantity
                total += subtotal
                print(f"\n{product.name} \n- Quantity: {quantity} \n- ${product.price:.2f} each \n- Subtotal: ${subtotal:.2f}")
                
            print(f"\nTotal: ${total:.2f}\n")
        
            print("Cart Options:")
            print("1. Update Quantity")
            print("2. Remove Item")
            print("3. Clear Cart")
            print("4. Proceed to checkout")
            print("5. Continue Shopping")
            choice = input("Enter a choice: ").strip()
        
            if choice == "1":
                self.update_cart_quantity()
            elif choice == "2":
                self.remove_from_cart()
            elif choice == "3":
                self.cart.clear()
                print("\nShopping cart cleared.")
                break
            elif choice == "4":
                self.checkout()
                break
            elif choice == "5":
                break
            else: 
                print("Invalid choice. Please enter a number between 1 and 5.")
                
                
    def update_cart_quantity(self):
        if not self.cart.items:
            print("Cart is empty.")
            return

        products = list(self.cart.items.keys())
        
        print("\n--- Update Cart Quantity ---")
        for i, product in enumerate(products, 1):
            print(f"{i}. {product.name} (Current quantity: {self.cart.items[product]})")

        while True:

            try:
                choice_input = input("Select item to update (or type 'exit' to cancel): ").strip()

                if choice_input.lower() == "exit":
                    print("\nUpdating cancelled.")
                    break
                
                choice = int(choice_input)

                if 1 <= choice <= len(products):
                    product = products[choice - 1]

                    while True:
                        try:
                            new_quantity_input = input("\nEnter new quantity (or type 'exit' to cancel): ").strip()
                            if new_quantity_input.lower() == 'exit':
                                print("\nUpdating quantity cancelled.")
                                return
                            
                            new_quantity = int(new_quantity_input)
                
                
                            if new_quantity == 0:
                                self.cart.remove_product(product)
                                print(f"\n'{product.name}' removed from cart.")
                                break
                            elif new_quantity > 0:
                                if new_quantity > product.stock:
                                    print(f"\nSorry, only {product.stock} in stock right now.")
                                else:
                                    self.cart.update_quantity(product, new_quantity)
                                    print("\nQuantity updated. Returning to cart...")
                                    break 
                            else:
                                print("\nInvalid quantity. Must be 0 or more.\n")
                        except ValueError:
                            print("\nInvalid input. Please enter a number.")

                    break
                else:
                    print("\nInvalid selection.\n")
            except ValueError:
                print("\nInvalid input. Please enter a valid number.\n")
                
    def remove_from_cart(self):
        if not self.cart.items:
            print("Cart is empty.")
            return
        
        while True:
            try:
                print("\nProducts in cart:")
                for i, (product, quantity) in enumerate(self.cart.items.items(), 1):
                    print(f"{i}. {product.name} - Quantity: {quantity}")
                
                choice_input = input("\nSelect product number to remove (or type 'exit' to exit): ").strip()
                if choice_input.lower() == "exit":
                    print("\nReturn to shopping cart.")
                    return
                
                choice = int(choice_input)
                products = list(self.cart.items.keys())
                
                if 1 <= choice <= len(products):
                    product = products[choice - 1]
                    self.cart.remove_product(product)
                    print(f"\nRemoved {product.name} from cart.")
                    
                    if not self.cart.items:
                        print("\nCart is now empty.")
                        return
                else:
                    print("\nInvalid selection.")
                    continue
            except ValueError:
                print("\nInvalid input. Please enter a number.")
                
                
    # Need to add function to proceed to checkout
    
    def update_profile(self):
        print("\n--- Update Profile ---")
        print("Leave blank to keep current value.")
        
        name = input(f"\nName [{self.current_customer.name}]: ").strip()
        while True:
            email = input(f"\nEmail [{self.current_customer.email}]: ").strip()
            if email:
                existing_customer = self.shop.find_customer_by_email(email)
                if existing_customer and existing_customer.user_id != self.current_customer.user_id:
                    print("\nEmail already taken by another customer. Try again or leave blank to keep current.")
                    continue
            break

        password = input("\nNew Password (leave blank to keep current): ").strip()
        address = input(f"\nAddress [{self.current_customer.address}]: ").strip()
        
        self.current_customer.update_profile(name, email, password)
        if address:
            self.current_customer.update_address(address)

        print("\nProfile updated successfully!")