from utils.helpers import (
    blue,
    red,
    green,
    reset,
    input_quit_handle,
    clear,
    typing_effect,
)
from db.db_operations import read_db, update_db, delete_db


def menu_admin_login():
    # Testing
    while True:
        action = input_quit_handle(
            green + f"What do you want to do? \n"
            "(1) Manage Users\n"
            "(2) Auction Items\n"
            "(3) logout\n"
            "Enter your choice admin: "
        ).strip()

        if action == "1":
            clear()
            manage_users()
        elif action == "2":
            clear()
            # Need to work on this option!
            # Comes when game is work due to in game updates and delete_db
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
        print(green + f"User Details for {user['name']}:" + reset)
        print(f"Name: {user['name']}")
        print(f"Email: {user['email']}")

        action = input_quit_handle(
            "(1) Modify Details\n"
            "(2) View/Modify Inventory\n"
            "(3) Back to Users Menu\n"
            "Enter your choice: "
        ).strip()

        if action == "1":
            modify_user_details(user)
        elif action == "2":
            manage_user_inventory(user["_id"])
        elif action == "3":
            return
        else:
            print(red + "Invalid choice. Please try again." + reset)


def modify_user_details(user):

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
            return

        print(green + "User Inventory:" + reset)
        for idx, item in enumerate(inventory, start=1):
            print(f"({idx}) {item['item_name']} - {item['quantity']}")

        print(f"({len(inventory) + 1}) Back to User Menu")

        choice = input_quit_handle("Select an item to modify or go back: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(inventory):
            modify_inventory_item(inventory[int(choice) - 1])
        elif choice == str(len(inventory) + 1):
            return
        else:
            print(red + "Invalid input. Please try again." + reset)


def modify_inventory_item(item):
    clear()
    print(green + f"Modify Inventory Item: {item['item_name']}" + reset)
    new_quantity = input(f"Enter new quantity (current: {item['quantity']}): ").strip()

    if new_quantity.isdigit():
        update_db("inventory", {"_id": item["_id"]}, {"quantity": int(new_quantity)})
        print(green + "Inventory item updated successfully!" + reset)
    else:
        print(red + "Invalid input. Quantity must be a number." + reset)
