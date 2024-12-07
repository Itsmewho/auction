from utils.helpers import (
    blue,
    red,
    green,
    reset,
    input_quit_handle,
    clear,
    typing_effect,
    handle_quit,
)
from db.db_operations import read_db, update_db, delete_db, insert_db


def menu_admin_login():
    # Testing
    while True:
        clear()
        action = input_quit_handle(
            green + f"What do you want to do? \n"
            "(1) Manage Users\n"
            "(2) Auction Items\n"
            "(3) logout\n"
            "(4) exit\n"
            "Enter your choice admin: "
        ).strip()

        if action == "1":
            clear()
            manage_users()
        elif action == "2":
            clear()
            manage_auction()
        elif action == "3":
            typing_effect(green + f"Logging out,.{reset}")
            clear()
            return
        elif action == "4":
            handle_quit()
            break
        else:
            typing_effect(red + f"Invalid choice. Please try again,.")
            clear()


def manage_users():

    while True:
        clear()
        users = read_db("users")
        if not users:
            print(blue + f"No users found!{reset}")
            return

        print(green + f"{reset}")
        for idx, user in enumerate(users, start=1):
            print(f"({idx}) {user['name']} - {user['email']}")

        print(f"({len(users) + 1}) Back to Main Menu")

        choice = input_quit_handle("Select a user or go back").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(users):
            manage_user_detail(users[int(choice) - 1])
        elif choice == str(len(users) + 1):
            return
        else:
            clear()
            print(red + f"Invalid choice. Please try again.{reset}")


def manage_user_detail(user):

    while True:
        clear()
        print(green + f"User Details for {user['name']}:{reset}")
        print(blue + f"Name: {user['name']}")
        print(f"Email: {user['email']}{reset}")

        action = input_quit_handle(
            "(1) Modify Details\n"
            "(2) View/Modify Inventory\n"
            "(3) Delete User\n"
            "(4) Back to Users Menu\n"
            "Enter your choice: "
        ).strip()

        if action == "1":
            modify_user_details_inner(user)
        elif action == "2":
            manage_user_inventory(user["_id"])
        elif action == "3":
            delete_user(user)
        elif action == "4":
            return
        else:
            print(red + "Invalid choice. Please try again." + reset)


def modify_user_details_inner(user):

    clear()
    print(green + f"Modify Details for {user['name']}:" + reset)
    new_name = input_quit_handle(
        f"Enter new name (leave blank to keep '{user['name']}'): "
    ).strip()
    new_email = input_quit_handle(
        f"Enter new email (leave blank to keep '{user['email']}'): "
    ).strip()

    updated_user = {
        "name": new_name if new_name else user["name"],
        "email": new_email if new_email else user["email"],
    }

    update_db("users", {"_id": user["_id"]}, updated_user)
    print(green + "User details updated successfully!" + reset)


def manage_user_inventory(user_id):

    while True:
        clear()
        inventory = read_db("inventory", {"user_id": user_id})
        if not inventory:
            print(red + "No inventory found for this user." + reset)

        print(green + "User Inventory:" + reset)
        for idx, item in enumerate(inventory, start=1):
            print(f"({idx}) {item['item']} - {item['sellprice']}")

        print(f"({len(inventory) + 1}) Add Item")
        print(f"({len(inventory) + 2}) Back to User Menu")

        choice = input_quit_handle(
            "Select an item to modify, add items, or go back: "
        ).strip()

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(inventory):
                modify_inventory_item(inventory[choice - 1])
            elif choice == len(inventory) + 1:
                add_inventory(user_id)
            elif choice == len(inventory) + 2:
                return
            else:
                print(red + "Invalid input. Please try again." + reset)
        else:
            print(red + "Invalid input. Please try again." + reset)


def add_inventory(user_id):
    clear()
    print(green + "Add New Inventory Item:" + reset)

    item = input_quit_handle("Enter item name: ").strip()
    sellprice = input_quit_handle("Enter sellprice: ").strip()

    if not item or not sellprice.isdigit():
        print(red + f"Invalid input. Please provide a valid name and price{reset}")
        return

    new_item = {"user_id": user_id, "item": item, "sellprice": float(sellprice)}

    insert_db("inventory", new_item)
    print(green + f"Item '{item}' added successfully!" + reset)


def modify_inventory_item(item):

    clear()
    print(green + f"Modify Inventory Item: {item['item']}" + reset)
    print(f"Sellprice Price: {item['sellprice']}")

    action = input_quit_handle(
        "(1) Update Sell Price\n"
        "(2) Delete Item\n"
        "(4) Back to Inventory Menu\n"
        "Enter your choice: "
    ).strip()

    if action == "1":
        sell_price(item)
    if action == "2":
        delete_item(item)
    elif action == "3":
        return
    else:
        print(red + "Invalid choice. Please try again." + reset)


def sell_price(item):
    new_price = input_quit_handle(
        f"Enter new starting price (current: {item['sellprice']}): "
    ).strip()
    if new_price.isdigit():
        update_db("inventory", {"_id": item["_id"]}, {"sellprice": float(new_price)})
        print(green + "Starting price updated successfully!" + reset)
    else:
        print(red + "Invalid input. Price must be a number." + reset)


def delete_item(item):
    delete_confirmation = (
        input_quit_handle(
            red
            + f"Are you sure you want to delete '{item['item']}'? (yes/no): "
            + reset
        )
        .strip()
        .lower()
    )
    if delete_confirmation == "yes":
        delete_db("inventory", {"_id": item["_id"]})
        print(green + f"Item '{item['item']}' deleted successfully!" + reset)


def delete_user_and_inventory(user_id):
    delete_db("users", {"_id": user_id})
    delete_db("inventory", {"user_id": user_id})


def delete_user(user):
    clear()
    delete_confirmation = (
        input_quit_handle(
            red
            + f"Are you sure you want to delete user '{user['name']}'? (yes/no): "
            + reset
        )
        .strip()
        .lower()
    )
    if delete_confirmation == "yes":
        delete_user_and_inventory(user["_id"])
        typing_effect(
            green
            + f"User '{user['name']}' and their inventory deleted successfully!"
            + reset
        )
        return
    else:
        print(blue + "Delete action cancelled." + reset)


def manage_auction():
    while True:
        clear()
        auction_items = read_db("auction_items")
        if not auction_items:
            print(blue + "No items found! Add some to get started." + reset)

        print(green + "Auction Items:" + reset)
        for idx, item in enumerate(auction_items, start=1):
            print(f"({idx}) {item['item']} - ${item['price']}")

        print(f"({len(auction_items) + 1}) Add Item")
        print(f"({len(auction_items) + 2}) Back to Main Menu")

        choice = input_quit_handle(
            "Select an item to manage or add a new one: "
        ).strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(auction_items):
                manage_auction_detail(auction_items[choice - 1])
            elif choice == len(auction_items) + 1:
                add_auction_inventory()
            elif choice == len(auction_items) + 2:
                return
            else:
                print(red + "Invalid choice. Please try again." + reset)
        else:
            print(red + "Invalid input. Please try again." + reset)


def manage_auction():
    while True:
        clear()
        auction_items = read_db("auction_items")
        if not auction_items:
            print(blue + "No items found! Add some to get started." + reset)

        print(green + "Auction Items:" + reset)
        for idx, item in enumerate(auction_items, start=1):
            print(f"({idx}) {item['item']} - ${item['price']}")

        print(f"({len(auction_items) + 1}) Add Item")
        print(f"({len(auction_items) + 2}) Back to Main Menu")

        choice = input_quit_handle(
            "Select an item to manage or add a new one: "
        ).strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(auction_items):
                manage_auction_detail(auction_items[choice - 1])
            elif choice == len(auction_items) + 1:
                add_auction_inventory()
            elif choice == len(auction_items) + 2:
                return
            else:
                print(red + "Invalid choice. Please try again." + reset)
        else:
            print(red + "Invalid input. Please try again." + reset)


def manage_auction_detail(auction_item):
    while True:
        clear()
        print(green + f"Auction item: {auction_item['item']}:" + reset)
        print(blue + f"Price: {auction_item['price']}" + reset)

        action = input_quit_handle(
            "(1) Modify Details\n"
            "(2) Delete Item\n"
            "(3) Go Back\n"
            "Enter your choice: "
        ).strip()

        if action == "1":
            modify_auction_details_inner(auction_item)
        elif action == "2":
            delete_auction_item(auction_item)
        elif action == "3":
            return
        else:
            print(red + "Invalid choice. Please try again." + reset)


def delete_auction_item(auction_item):
    delete_confirmation = (
        input_quit_handle(
            red
            + f"Are you sure you want to delete '{auction_item['item']}'? (yes/no): "
            + reset
        )
        .strip()
        .lower()
    )
    if delete_confirmation == "yes":
        delete_auction_item(auction_item["_id"])
        print(green + f"Item '{auction_item['item']}' deleted successfully!" + reset)
        return


def validate_price(price_input):
    try:
        price = float(price_input)
        if price < 0:
            print(red + "Price must be a positive number." + reset)
            return None
        return price
    except ValueError:
        print(red + "Invalid price. Please enter a valid number." + reset)
        return None


def modify_auction_details_inner(auction_item):
    clear()
    print(green + f"Modify details for {auction_item['item']}:" + reset)
    new_item_name = input_quit_handle(
        f"Enter new item name (leave blank to keep '{auction_item['item']}'): "
    ).strip()
    new_price = input_quit_handle(
        f"Enter new price (leave blank to keep '{auction_item['price']}'): "
    ).strip()

    updated_item = {
        "item": new_item_name if new_item_name else auction_item["item"],
        "price": float(new_price) if new_price.isdigit() else auction_item["price"],
    }

    update_db("auction_items", {"_id": auction_item["_id"]}, updated_item)
    print(green + "Auction item details updated successfully!" + reset)


def add_auction_inventory():
    clear()
    print(green + "Add New Auction Item:" + reset)

    item = input_quit_handle("Enter item name: ").strip()
    price = input_quit_handle("Enter price: ").strip()

    if not price.isdigit():
        print(red + "Invalid input. Please provide a valid numeric price." + reset)
        return

    new_item = {"item": item, "price": float(price)}

    insert_db("auction_items", new_item)
    print(green + f"Item '{item}' added successfully!" + reset)


def delete_auction_item(auction_id):
    delete_db("auction_items", {"_id": auction_id})
