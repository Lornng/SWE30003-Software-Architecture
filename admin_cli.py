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
            print("4. Manage Deliveries")
            print("5. Logout")
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.manage_products()
            elif choice == "2":
                self.view_customer_orders()
            elif choice == "3":
                self.generate_sales_report()
            elif choice == "4":
                self.manage_deliveries() 
            elif choice == "5":
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
            
            
    def manage_deliveries(self):
        while True:
            print("\n--- Delivery Management ---")
            print("1. View All Deliveries")
            print("2. Search Delivery to Update Status")
            print("3. Back to Admin Menu")
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.view_all_deliveries()
            elif choice == "2":
                self.search_delivery_update_status()
            elif choice == "3":
                break
            else:
                print("\nInvalid choice. Please enter 1-3.")

    def view_all_deliveries(self):
        print("\n--- All Deliveries ---")
        
        deliveries = []
        for order in self.shop.orders:
            if hasattr(order, 'delivery') and order.delivery:
                deliveries.append((order.order_id, order.delivery))
        
        if not deliveries:
            print("\nNo deliveries found.")
            return
        
        print(f"{'Order ID':<12} {'Tracking_No':<15} {'Status':<15} {'Method':<12} {'Address':<30}")
        print("-" * 90)
        
        for order_id, delivery in deliveries:
            print(f"{order_id:<12} {delivery.tracking_number:<15} {delivery.status:<15} "
                f"{delivery.method:<12} {delivery.address[:30]:<30}")

    def search_delivery_update_status(self):
        print("\n--- Search Delivery To Update Status ---")
        while True:
            search_term = input("\nEnter tracking number or order ID (or type 'exit' to cancel): ").strip()
            
            if not search_term:
                print("\nSearch term cannot be empty.")
                continue
            if search_term.lower() == 'exit':
                print("\nReturn to delivery Managment menu...")
                return
            
            found_deliveries = []
            
            for order in self.shop.orders:
                if hasattr(order, 'delivery') and order.delivery:
                    # Search by tracking number or order ID
                    if (search_term.upper() in order.delivery.tracking_number.upper() or 
                        search_term.upper() in order.order_id.upper()):
                        found_deliveries.append((order, order.delivery))
            
            if not found_deliveries:
                print(f"\nNo deliveries found matching '{search_term}'")
                continue
            
            print(f"\nFound {len(found_deliveries)} delivery(s):")
            print("-" * 80)
            
            for i, (order, delivery) in enumerate(found_deliveries, 1):
                print(f"\n{i}. Order ID: {order.order_id}")
                print(f"   Tracking Number: {delivery.tracking_number}")
                print(f"   Current Status: {delivery.status}")
                print(f"   Method: {delivery.method}")
                print(f"   Address: {delivery.address}")
                print(f"   Estimated Delivery: {delivery.estimated_delivery}")
            
            # Option to update status of found delivery
            if len(found_deliveries) == 1:
                choice = input(f"\nUpdate status for this delivery? (y/n): ").strip().lower()
                if choice == 'y':
                    self.update_specific_delivery_status(found_deliveries[0][1])
            elif len(found_deliveries) > 1:
                try:
                    choice = input(f"\nSelect delivery to update (1-{len(found_deliveries)}) or 0 to cancel: ").strip()
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(found_deliveries):
                        self.update_specific_delivery_status(found_deliveries[choice_num-1][1])
                    elif choice_num != 0:
                        print("\nInvalid selection.")
                except ValueError:
                    print("\nInvalid input. Please select enter a number")


    def update_specific_delivery_status(self, delivery):
        """Update status for a specific delivery"""
        print(f"\n--- Update Status for Tracking #{delivery.tracking_number} ---")
        print(f"Current Status: {delivery.status}")
        
        # Valid status options
        valid_statuses = ["Processing", "Shipped", "In Transit", "Out for Delivery", "Delivered", "Delayed"]
        
        print("\nAvailable Status Options:")
        for i, status in enumerate(valid_statuses, 1):
            print(f"{i}. {status}")
        
        try:
            choice = input(f"\nSelect new status (1-{len(valid_statuses)}) or 0 to cancel: ").strip()
            choice_num = int(choice)
            
            if choice_num == 0:
                print("Status update cancelled.")
                return
            elif 1 <= choice_num <= len(valid_statuses):
                new_status = valid_statuses[choice_num-1]
                
                # Confirm the change
                print(f"\nConfirm status change:")
                print(f"From: {delivery.status}")
                print(f"To:   {new_status}")
                
                confirm = input("Proceed with update? (y/n): ").strip().lower()
                if confirm == 'y':
                    try:
                        delivery.update_status(new_status)
                        print(f"\n Delivery status updated successfully!")
                        print(f"Tracking #{delivery.tracking_number} is now: {new_status}")
                        
                        # Save changes to file
                        self.shop.save_data()
                        print("Changes saved to database.")
                        
                    except ValueError as e:
                        print(f"Error updating status: {e}")
                else:
                    print("Status update cancelled.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
                
                
        