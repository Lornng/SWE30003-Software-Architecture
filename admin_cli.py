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
            name = input("Product name (or 'exit' to cancel): ").strip()
            if name.lower() == 'exit':
                print("Add product cancelled.")
                return
            description = input("Description (or 'exit' to cancel): ").strip()
            if description.lower() == 'exit':
                print("Add product cancelled.")
                return
            price_input = input("Price (or 'exit' to cancel): ").strip()
            if price_input.lower() == 'exit':
                print("Add product cancelled.")
                return
            price = float(price_input)
            stock_input = input("Stock quantity (or 'exit' to cancel): ").strip()
            if stock_input.lower() == 'exit':
                print("Add product cancelled.")
                return
            stock = int(stock_input)
            category = input("Category (or 'exit' to cancel): ").strip()
            if category.lower() == 'exit':
                print("Add product cancelled.")
                return

            existing_ids = [
                int(p.product_id[1:]) for p in self.shop.products
                if isinstance(p.product_id, str) and p.product_id.startswith('P') and p.product_id[1:].isdigit()
            ]
            next_id_num = max(existing_ids, default=0) + 1
            product_id = f"P{next_id_num:03d}"

            print("\nPlease confirm the following product details:")
            print(f"ID: {product_id}")
            print(f"Name: {name}")
            print(f"Description: {description}")
            print(f"Price: ${price:.2f}")
            print(f"Stock: {stock}")
            print(f"Category: {category}")
            confirm = input("Add this product? (y/n): ").strip().lower()
            if confirm == 'y':
                product = Product(product_id, name, description, price, stock, category)
                self.shop.add_product(product)
                print("Product added successfully.")
            else:
                print("Add product cancelled.")
        except ValueError:
            print("Invalid input. Please enter correct values.")


    def modify_product(self):
        print("\n--- Modify Product ---")
        self.list_products()
        try:
            pid_input = input("Enter Product ID to modify (or 'exit' to cancel): ").strip()
            if pid_input.lower() == 'exit':
                print("Modify product cancelled.")
                return
            pid = pid_input
            product = self.shop.find_product_by_id(pid)
            if not product:
                print("Product not found.")
                return
            print("Leave blank to keep current value. Type 'exit' to cancel.")
            name = input(f"New name [{product.name}]: ").strip()
            if name.lower() == 'exit':
                print("Modify product cancelled.")
                return
            description = input(f"New description [{product.description}]: ").strip()
            if description.lower() == 'exit':
                print("Modify product cancelled.")
                return
            price_input = input(f"New price [{product.price}]: ").strip()
            if price_input.lower() == 'exit':
                print("Modify product cancelled.")
                return
            stock_input = input(f"New stock [{product.stock}]: ").strip()
            if stock_input.lower() == 'exit':
                print("Modify product cancelled.")
                return
            category = input(f"New category [{product.category}]: ").strip()
            if category.lower() == 'exit':
                print("Modify product cancelled.")
                return

            new_name = name or product.name
            new_description = description or product.description
            new_price = float(price_input) if price_input else product.price
            new_stock = int(stock_input) if stock_input else product.stock
            new_category = category or product.category

            print("\nPlease confirm the following changes:")
            print(f"Name: {new_name}")
            print(f"Description: {new_description}")
            print(f"Price: ${new_price:.2f}")
            print(f"Stock: {new_stock}")
            print(f"Category: {new_category}")
            confirm = input("Apply these changes? (y/n): ").strip().lower()
            if confirm == 'y':
                self.shop.modify_product(pid, name=new_name, description=new_description,
                                        price=new_price, stock=new_stock, category=new_category)
                print("Product updated successfully.")
            else:
                print("Modify product cancelled.")
        except ValueError:
            print("Invalid input.")

    def delete_product(self):
        print("\n--- Delete Product ---")
        self.list_products()
        try:
            pid_input = input("Enter Product ID to delete (or 'exit' to cancel): ").strip()
            if pid_input.lower() == 'exit':
                print("Delete product cancelled.")
                return
            pid = pid_input
            product = self.shop.find_product_by_id(pid)
            if not product:
                print("Product not found.")
                return
            print("\nPlease confirm deletion of the following product:")
            print(product)
            confirm = input("Delete this product? (y/n): ").strip().lower()
            if confirm == 'y':
                if self.shop.delete_product(pid):
                    print("Product deleted successfully.")
                else:
                    print("Product not found.")
            else:
                print("Delete product cancelled.")
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
