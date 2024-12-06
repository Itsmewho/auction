from utils.helpers import (
    blue,
    red,
    green,
    reset,
    input_quit_handle,
    clear,
    typing_effect,
)
from db.db_operations import read_db, update_db, delete_db, insert_db
import sha


def menu_admin_login():
    # Testing
    while True:
        action = input_quit_handle(
            green + f"What do you want to do? \n"
            "(1) Manage Users\n"
            "(2) Auction Items\n"
            "(4) logout\n"
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
        new_price = input_quit_handle(
            f"Enter new starting price (current: {item['sellprice']}): "
        ).strip()
        if new_price.isdigit():
            update_db(
                "inventory", {"_id": item["_id"]}, {"sellprice": float(new_price)}
            )
            print(green + "Starting price updated successfully!" + reset)
        else:
            print(red + "Invalid input. Price must be a number." + reset)

    if action == "2":
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
    elif action == "3":
        return
    else:
        print(red + "Invalid choice. Please try again." + reset)


def delete_user_and_inventory(user_id):
    # Delete user everywhere in the DB
    delete_db("users", {"_id": user_id})
    delete_db("inventory", {"user_id": user_id})


def manage_auction():

    while True:
        auction_items = read_db("auction_items")
        if not auction_items:
            print(blue + f"No items found! {reset}")
            return

        print(green + f"{reset}")
        for idx, item in enumerate(auction_items, start=1):
            print(f"({idx}) {item["item"]} = {item["price"]}")

        print(f"({len(auction_items) + 1} Back to Main Menu")

        choice = input_quit_handle("Select a item or go back").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(auction_items):
            manage_auction_detail(auction_items[int(choice) - 1])
        elif choice == str(len(auction_items) + 1):
            return
        else:
            print(red + f"Invalid choice. Please try again. {reset}")


def manage_auction_detail(auction_item):

    while True:
        clear()
        print(green + f"Auction item: {auction_item["item"]}: {reset}")
        print(blue + f"Price: {auction_item["price"]}")

        action = input_quit_handle(
            "(1) Modify Detail\n"
            "(2) Add Items\n"
            "(2) Delete Items\n"
            "(4) Go back\n"
            "Enter your choice\n"
        ).strip()
        if action == "1":
            modify_aution_details_inner(auction_item)
        elif action == "2":
            manage_auction_inventory(auction_item["_id"])
        elif action == "3":
            clear()
            delete_confirmation = (
                input_quit_handle(
                    red
                    + f"Are you sure you want to delete item '{auction_item['name']}'? (yes/no): "
                    + reset
                )
                .strip()
                .lower()
            )
            if delete_confirmation == "yes":
                delete_auction_item(auction_item["_id"])
                typing_effect(
                    green
                    + f"Auction item: '{auction_item['name']}' deleted successfully!"
                    + reset
                )
                return
            else:
                print(blue + "Delete action cancelled." + reset)
        elif action == "4":
            return
        else:
            print(red + "Invalid choice. Please try again." + reset)


def modify_aution_details_inner(auction_item):

    clear()
    print(green + f"Modify details for {auction_item["item"]}{reset}")
    new_name = input_quit_handle(
        f"Enter new name (leave blank to keep '{auction_item['name']}'): "
    ).strip()
    new_price = input_quit_handle(
        f"Enter new price (leave blank to keep '{auction_item['price']}'): "
    ).strip()

    updated_item = {
        "name": new_name if new_name else auction_item["name"],
        "price": new_price if new_price else auction_item["price"],
    }
    # Add check input is str or int
    update_db("autcion_items", {"_id": auction_item["_id"]}, updated_item)
    print(green + "Details updated successfully!" + reset)


def manage_auction_inventory(item_id):
    # Add of go back.
    print()


def delete_auction_item(auction_id):
    # Delete auction items only in the item-collection
    delete_db("auction_items", {"_id": auction_id})
