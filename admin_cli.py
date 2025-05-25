from shop import Shop
from product import Product

class AdminCLI:
    def __init__(self, shop):
        self.shop = shop
        self.current_admin = None

    def run(self):
        if not self.login():
            print("Admin authentication failed.")
            return

        while True:
            print("\n--- Admin Menu ---")
            print("1. Manage Products")
            print("2. View Customer Orders")
            print("3. Generate Sales Report")
            print("4. Logout")
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.manage_products()
            elif choice == "2":
                self.view_customer_orders()
            elif choice == "3":
                self.generate_sales_report()
            elif choice == "4":
                print("Logging out of admin account.")
                self.current_admin = None
                break
            else:
                print("Invalid choice. Please enter 1-4.")

    def login(self):
        print("\n--- Admin Login ---")
        email = str(input("Admin email: ").strip())
        password = str(input("Password: ").strip())
        admin = self.shop.find_admin_by_email(email)
        if admin and admin.password == password:
            self.current_admin = admin
            print(f"Welcome, {admin.name}!")
            return True
        else:
            print("Incorrect email or password.")
            return False

    def manage_products(self):
        while True:
            print("\n--- Product Management ---")
            print("1. Add Product")
            print("2. Modify Product")
            print("3. Delete Product")
            print("4. List All Products")
            print("5. Back to Admin Menu")
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.add_product()
            elif choice == "2":
                self.modify_product()
            elif choice == "3":
                self.delete_product()
            elif choice == "4":
                self.list_products()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please enter 1-5.")

    def add_product(self):
        print("\n--- Add New Product ---")
        try:
            name = input("Product name: ").strip()
            description = input("Description: ").strip()
            price = float(input("Price: ").strip())
            stock = int(input("Stock quantity: ").strip())
            category = input("Category: ").strip()
            product_id = max([p.product_id for p in self.shop.products], default=0) + 1
            product = Product(product_id, name, description, price, stock, category)
            self.shop.add_product(product)
            print("Product added successfully.")
        except ValueError:
            print("Invalid input. Please enter correct values.")

    def modify_product(self):
        print("\n--- Modify Product ---")
        self.list_products()
        try:
            pid = int(input("Enter Product ID to modify: ").strip())
            product = self.shop.find_product_by_id(pid)
            if not product:
                print("Product not found.")
                return
            print("Leave blank to keep current value.")
            name = input(f"New name [{product.name}]: ").strip() or product.name
            description = input(f"New description [{product.description}]: ").strip() or product.description
            price_input = input(f"New price [{product.price}]: ").strip()
            price = float(price_input) if price_input else product.price
            stock_input = input(f"New stock [{product.stock}]: ").strip()
            stock = int(stock_input) if stock_input else product.stock
            category = input(f"New category [{product.category}]: ").strip() or product.category
            self.shop.modify_product(pid, name=name, description=description, price=price, stock=stock, category=category)
            print("Product updated successfully.")
        except ValueError:
            print("Invalid input.")

    def delete_product(self):
        print("\n--- Delete Product ---")
        self.list_products()
        try:
            pid = int(input("Enter Product ID to delete: ").strip())
            if self.shop.delete_product(pid):
                print("Product deleted successfully.")
            else:
                print("Product not found.")
        except ValueError:
            print("Invalid input.")

    def list_products(self):
        print("\n--- Product List ---")
        if not self.shop.products:
            print("No products available.")
        else:
            for product in self.shop.products:
                print(product)

    def view_customer_orders(self):
        print("\n--- Customer Orders ---")
        customers = self.shop.list_customers()
        if not customers:
            print("No customers found.")
            return
        for idx, customer in enumerate(customers, 1):
            print(f"{idx}. {customer.name} ({customer.email})")
        try:
            choice = int(input("Select customer by number: ").strip())
            if 1 <= choice <= len(customers):
                customer = customers[choice - 1]
                orders = self.shop.list_orders_by_customer(customer)
                if not orders:
                    print("No orders for this customer.")
                else:
                    for order in orders:
                        print(order)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")

    def generate_sales_report(self):
        print("\n--- Sales Report ---")
        from datetime import datetime
        start_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date_str = input("Enter end date (YYYY-MM-DD): ").strip()
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            orders = [o for o in self.shop.orders if start_date <= o.order_date <= end_date]
            total_sales = sum(o.total_price for o in orders)
            print(f"Total orders: {len(orders)}")
            print(f"Total sales: ${total_sales:.2f}")
        except ValueError:
            print("Invalid date format.")
