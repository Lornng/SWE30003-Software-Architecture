from cart import Cart
from customer import Customer
from datetime import datetime
import random


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
        
        credentials = self.get_login_credentials()
        if not credentials:
            return
            
        email, password = credentials
        
        # Authenticate user
        customer = self.shop.authenticate_customer(email, password)
        if customer:
            self.current_customer = customer
        else:
            print("\nInvalid email or password. Please try again.")
            
    def get_login_credentials(self):
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
            
        return email, password

    def register(self):
        print("\n--- Customer Registration ---")
        print("\nType 'exit' at any prompt to cancel registration.")
        
        user_data = self.get_register_data()
        if not user_data:
            return
        
        success, message = self.shop.register_customer(user_data)
        if success:
            print("\nRegistration successful! You can now login.")
        else:
            print(f"\nRegistration failed: {message}")
            
        
    def get_register_data(self):
        try:
            # Full Name prompt and format validation
            while True:
                name = input("\nFull Name: ").strip()
                if name.lower() == 'exit':
                    print("\nRegistration cancelled.")
                    return
                if not name:
                    print("\nName is required.")
                    continue
                is_valid, error_msg = self.shop.validate_name(name)
                if not is_valid:
                    print(f"\n{error_msg}")
                    continue
                break
            
            # Email prompt and format validation
            while True: 
                email = input("\nEmail: ").strip()
                if email.lower() == 'exit':
                    print("\nRegistration cancelled.")
                    return
                if not email:
                    print("\nEmail is required.")
                    continue
                # Email format validation
                is_valid, error_msg = self.shop.validate_email_for_register(email)
                if not is_valid:
                    print(f"\n{error_msg}")
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
                is_valid, error_msg = self.shop.validate_password(password)
                if not is_valid:
                    print(f"\n{error_msg}")
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
                
            return (name, email, password, address)
            
        except Exception as e:
            print(f"\nError collecting registration data: {e}")
            return None
            
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
                print(f"Logging out of {self.current_customer.name} account .")
                self.current_customer = None
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
        
        self.display_products(products)
        self.add_to_cart_prompt(products)
        
    def display_products(self, products):
        for product in products:
            print(product)
            print("-" * 50)
                    
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
                self.display_products(products)
                self.add_to_cart_prompt(products)
                print("\n--- Search again or type 'exit' to leave ---\n")
                
                
    # Browse products by category
    def browse_by_category(self):
        print("\n--- Browse products by Category ---")
        
        # Get all categories
        categories = self.shop.get_product_categories()
        
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
            print("Invalid input. Please enter a number.")
            
    
    def add_to_cart_prompt(self, allowed_products = None):
        while True:
            choice = input("\nWould you like to add a product to cart? (y/n): ").strip().lower()
            if choice == 'n':
                break
            elif choice == 'y':
                self.add_to_cart(allowed_products)
                break
            else:
                print("\nPlease enter 'y' or 'n'.")
            
    def add_to_cart(self, allowed_products = None):
        while True:
            product_id_input = input("\nPlease enter Product ID to add to cart (or type 'exit' to cancel): ").strip()
            if product_id_input.lower() == 'exit':
                print("\nAdd item to cart cancelled.")
                return
               
            product_id = product_id_input.upper()
            product = self.shop.find_product_by_id(product_id)
                
            if not product:
                print("\nProduct not found. Please try again.")
                continue
                
            if allowed_products and not any(p.product_id == product.product_id for p in allowed_products):
                print("\nProduct not available in this view. Please select a valid product.")
                continue
            
            try:
                quantity_input = input(f"\nEnter quantity for '{product.name}' (stock: {product.stock}) (or type 'exit' to cancel): ").strip()
                    
                if quantity_input.lower() == 'exit':
                    print(f"\nAdd {product.name} to cart cancelled")
                    return
                    
                quantity = int(quantity_input)
                    
                self.cart.add_product(product, quantity)
                print(f"\nAdded {product.name} x {quantity} to cart.")
                    
                again = input("\nWould you like to add another product? (y/n): ").strip().lower()
                if again == 'n':
                    print("\nReturn to menu...")
                    break
                elif again == 'y':
                    continue
                else:
                    print("\nPlease enter 'y' or 'n'.")
                
            except ValueError as e:
                print(f"\nFailed to add product: {e}")
                
                
            
    """ 
    Displays the contents of the shopping cart and provides users with the option to update products quantity, 
    remove products, clear cart, proceed to checkout, or continue shopping.
    """
    def view_cart(self):

        while True:
            print("\n--- Your Shopping Cart ---")
            if self.cart.is_empty():
                print("Your cart is empty.")
                return
        
            summary = self.cart.get_cart_summary()
            self.display_cart_summary(summary)
        
            print("\nCart Options:")
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
                
    def display_cart_summary(self, summary):
        """Helper method to display cart summary - Pure UI"""
        for item in summary['items']:
            print(f"\n{item['name']}")
            print(f"- Quantity: {item['quantity']}")
            print(f"- ${item['price']:.2f} each")
            print(f"- Subtotal: ${item['subtotal']:.2f}")
        
        print(f"\nTotal: ${summary['total']:.2f}")
        print(f"Items: {summary['item_count']}")
        
    def update_cart_quantity(self):
        if self.cart.is_empty():
            return
        
        products = list(self.cart.items.keys())
        
        print("\n--- Update Quantity ---")
        for i, product in enumerate(products, 1):
            current_qty = self.cart.items[product]
            print(f"{i}. {product.name} (Current: {current_qty})")
        
        while True:
            try:
                choice_input = input("\nSelect item to update (or type 'exit' to cancel): ").strip()

                if choice_input.lower() == "exit":
                    print("\nUpdating cancelled. Returning to cart...")
                    break
                
                choice = int(choice_input)
                if 1 <= choice <= len(products):
                    product = products[choice - 1]
                    
                    new_quantity_input = input("\nEnter new quantity (or type 'exit' to cancel): ").strip()
                    if new_quantity_input.lower() == 'exit':
                        print("\nUpdating cancelled. Returning to cart...")
                        return
                        
                    new_quantity = int(new_quantity_input)
                    
                    try:
                        if new_quantity == 0:
                            self.cart.remove_product(product)
                            print(f"\n'{product.name}' removed from cart.")
                            break
                        else:
                            self.cart.update_quantity(product, new_quantity)
                            print("\nQuantity updated.")
                    except ValueError as e:
                        print(f"\nUpdate failed: {e}")
                else:
                    print("\nInvalid selection.")
            except ValueError:
                print("\nInvalid input. Please enter a number.")
                
    def remove_from_cart(self):
    
        while True:
            if self.cart.is_empty():
                return
        
            products = list(self.cart.items.keys())
        
            print("\n--- Remove Item ---")
            print("\nProducts in cart:")
            for i, product in enumerate(products, 1):
                print(f"{i}. {product.name}")
            
            try:
                choice_input = input("\nSelect product number to remove (or type 'exit' to exit): ").strip()
                if choice_input.lower() == "exit":
                    print("\nReturn to shopping cart.")
                    return
                
                choice = int(choice_input)
                
                if 1 <= choice <= len(products):
                    product = products[choice - 1]
                    self.cart.remove_product(product)
                    print(f"\nRemoved {product.name} from cart.")
                    continue
                else:
                    print("\nInvalid selection.")
                    continue
            except ValueError:
                print("\nInvalid input. Please enter a number.")
                    
                
    # ----------------Checkout Order ---------------
    def checkout(self):
        """Handle the checkout process including payment method selection"""
        # Check if cart is empty
        if self.cart.is_empty(): 
            print("Your cart is empty. Nothing to checkout.")
            return
        
        # Get payment method selection
        payment_method = self.get_payment_method()
       
        if not payment_method:
            print("Checkout cancelled.")
            return
        
        # Display checkout summary
        self.display_checkout_summary(payment_method)
        
        # Get final confirmation
        confirm = input("\nConfirm checkout? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Checkout cancelled.")
            return
        
        # Process the order
        try:
            order = self.shop.place_order(
                customer=self.current_customer,
                cart=self.cart,
                payment_method=payment_method
            )
            
            # Display result
            self.display_order_result(order)
            
        except Exception as e:
            print(f"\nError during checkout: {str(e)}")
            # Keep items in cart for retry
            print("Your items have been kept in the cart for your next attempt.")

    def get_payment_method(self):
        # Display available payment methods
        payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "Cash on Delivery"]
        print("\n--- Available Payment Methods ---")
        for i, method in enumerate(payment_methods, 1):
            print(f"{i}. {method}")
            
        while True:
            try:
                choice = input("\nSelect payment method (1-4): ").strip()
                if choice.lower() == 'exit':
                    return None
                    
                choice_num = int(choice)
                if 1 <= choice_num <= len(payment_methods):
                    return payment_methods[choice_num-1]
                else:
                    print(f"Please enter a number between 1 and {len(payment_methods)}")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
    def display_checkout_summary(self, payment_method):
        # Display cart summary
        summary = self.cart.get_cart_summary()
        print("\n--- Order Summary ---")
        print("Items in your cart:")
        for item in summary['items']:
            print(f"- {item['name']} x {item['quantity']}: ${item['subtotal']:.2f}")
        print(f"\nTotal: ${summary['total']:.2f}")
        print(f"Shipping to: {self.current_customer.address}")
        print(f"Payment Method: {payment_method}")
        
        
    def display_order_result(self, order):
        if order:
            if order.status == "Confirmed":
                print("\nOrder confirmed! Thank you for your purchase.")
                print(f"Order ID: {order.order_id}")
                print(f"Payment ID: {order.payment.payment_id}")
                print(f"Tracking Number: {order.delivery.tracking_number}")
                print(f"Estimated Delivery: {order.delivery.estimated_delivery.strftime('%Y-%m-%d')}")
            elif order.status == "Payment Failed":
                print("\nPayment failed. Please try a different payment method.")
                    # Keep items in cart for retry
            else:
                print(f"\nOrder status: {order.status}")
        else:
            print("\nFailed to place order. Please try again.")
            
    def update_profile(self):
        print("\n--- Update Profile ---")
        print("Leave blank to keep current value.")
        
        # Get input from user
        profile_data = self.get_profile_update_data()
        
        success, message = self.shop.update_customer_profile(self.current_customer, profile_data)
        if success:
            print("\nProfile updated successfully!")
        else:
            print(f"\nProfile update failed: {message}")
            
            
    def get_profile_update_data(self):
        while True:
            name = input(f"\nName [{self.current_customer.name}]: ").strip()
            if not name:
                name = None
                break
            
            is_valid, error_msg = self.shop.validate_name(name)
            if not is_valid:
                print(f"\n{error_msg}")
                continue
            break
                
        while True:
            email = input(f"\nEmail [{self.current_customer.email}]: ").strip()
            if not email:
                email = None
                break
            
            is_valid, error_msg = self.shop.validate_email_for_update(email, self.current_customer.user_id)
            if not is_valid:
                print(f"\n{error_msg}")
                continue
            break

        while True:
            password = input("\nNew Password (leave blank to keep current): ").strip()
            if not password:
                password = None
                break
            is_valid, error_msg = self.shop.validate_password(password)
            if not is_valid:
                print(f"\n{error_msg}")
                continue
            break
            
        while True:
            address = input(f"\nAddress [{self.current_customer.address}]: ").strip()
            if not address: 
                address = None
                break
            break
        
        return {
            'name': name or None,
            'email': email or None, 
            'password': password or None,
            'address': address or None
        }
        
        
    def view_order_history(self):
        orders = self.shop.list_orders_by_customer(self.current_customer)
        if not orders:
            print("\nNo orders found.")
            return
        
        print("\n--- Order History ---")
        for order in orders:
            print(order)
            print("-" * 50)
            
    
    
    def request_refund(self):
        print("\n--- Request Refund ---")
        orders = self.shop.list_orders_by_customer(self.current_customer)

        eligible_orders = [o for o in orders if o.status not in ("Refunded", "Cancelled", "Pending Refund")]
        if not eligible_orders:
            print("No orders eligible for refund.")
            return

        print("\nEligible Orders:")
        for idx, order in enumerate(eligible_orders, start=1):
            print(f"{idx}. Order ID: {order.order_id} | Status: {order.status} | Total: ${order.total_price:.2f}")

        try:
            choice = input("\nEnter the number of the order to refund (or type 'exit' to cancel): ").strip()
            if choice.lower() == "exit":
                print("Refund request cancelled.")
                return

            idx = int(choice) - 1
            if 0 <= idx < len(eligible_orders):
                order = eligible_orders[idx]
                order.update_status("Pending Refund", silent=True)
                print(f"Refund request submitted for Order ID: {order.order_id}. Awaiting admin approval.")
                self.shop.save_data()
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def logout(self):
        print("Logging out...")
        self.current_customer = None
        self.cart.clear() 
        