# main.py

from shop import Shop
from shop_cli import ShopCLI
from admin_cli import AdminCLI

def main():
    shop = Shop()
    shop.load_data()   

    while True:
        print("\nWelcome to the Online Electronics Store!")
        print("1. Customer Login/Register")
        print("2. Admin Login")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            cli = ShopCLI(shop)
            cli.run()
        elif choice == "2":
            admin_cli = AdminCLI(shop)
            admin_cli.run()
        elif choice == "3":
            print("End")
            shop.save_data()
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
