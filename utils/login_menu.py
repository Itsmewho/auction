# Log in menu
from utils.auction import auction
from utils.admin_menu import delete_user_and_inventory
from db.db_operations import read_db, update_db, delete_db, insert_db
from utils.helpers import (
    green,
    red,
    blue,
    reset,
    input_quit_handle,
    clear,
    handle_quit,
    typing_effect,
)


def menu_user_login(logged_user):

    while True:
        clear()
        action = input_quit_handle(
            green + f"What do you want to do? \n"
            "(1) Go to auction\n"
            "(2) See inventory\n"
            "(3) Sell items\n"
            "(4) Account details\n"
            "(5) Logout\n"
            "(6) Exit\n"
            "(7) Delete account\n"
            "Enter your choice: "
        ).strip()

        if action == "1":
            clear()
            auction(logged_user)
        elif action == "2":
            clear()
            see_inventory(logged_user)
        elif action == "3":
            clear()
            sell_items(logged_user)
        elif action == "4":
            view_account_details(logged_user)
        elif action == "5":
            typing_effect(green + f"Logging out,.{reset}")
            clear()
            return
        elif action == "6":
            handle_quit()
            break
        elif action == "7":
            clear()
            delete_account(logged_user)
            handle_quit()
        else:
            print("Invalid choice, please select again.")


def see_inventory(logged_user):
    while True:
        inventory = read_db("inventory", {"user_id": logged_user})
        if not inventory:
            print(red + "No inventory found for this user." + reset)

        print(green + "User Inventory:" + reset)
        for idx, item in enumerate(inventory, start=1):
            print(f"({idx}) {item['item']} - {item['sellprice']}")

        print(f"({len(inventory) + 1}) Back to User Menu")

        choice = input_quit_handle("Go back: ").strip()

        if choice.isdigit():
            choice = int(choice)
            if choice == len(inventory) + 1:
                clear()
                return
            else:
                print(red + "Invalid input. Please try again." + reset)
        else:
            print(red + "Invalid input. Please try again." + reset)


def sell_items(logged_user):
    while True:
        inventory = read_db("inventory", {"user_id": logged_user["_id"]})
        if not inventory:
            typing_effect(red + "No inventory found for this user." + reset)
            return

        print(green + "User Inventory:" + reset)
        for idx, item in enumerate(inventory, start=1):
            print(f"({idx}) {item['item']} - {item['sellprice']}")

        print(f"({len(inventory) + 1}) Back to User Menu")

        choice = input_quit_handle("Enter your choice: ").strip()

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(inventory):
                sell_inventory_item(inventory[choice - 1])
            elif choice == len(inventory) + 1:
                return
            else:
                print(red + "Invalid input. Please try again." + reset)
        else:
            print(red + "Invalid input. Please try again." + reset)


def sell_inventory_item(item):
    new_price = input_quit_handle(
        f"Enter new starting price for '{item['item']}' (current: {item['sellprice']}): "
    ).strip()

    if new_price.isdigit():
        new_price = float(new_price)
        update_db("inventory", {"_id": item["_id"]}, {"sellprice": new_price})
        print(green + "Starting price updated successfully!" + reset)
    else:
        print(red + "Invalid input. Price must be a number." + reset)

    sell_confirmation = (
        input_quit_handle(
            red
            + f"Are you sure you want to sell '{item['item']}' for {new_price}? (yes/no): "
            + reset
        )
        .strip()
        .lower()
    )

    if sell_confirmation == "yes":
        insert_db("auction_items", {"item": item["item"], "price": new_price})
        update_db("users", {"_id": item["user_id"]}, {"$inc": {"money": new_price}})
        delete_db("inventory", {"_id": item["_id"]})
        print(green + f"Item '{item['item']}' sold successfully!" + reset)
    else:
        print(red + "Sale canceled." + reset)


def view_account_details(logged_user):
    while True:
        clear()
        print(green + f"Viewing idetails for {logged_user['name']}..." + reset)
        print(blue + f"Name: {logged_user['name']}")
        print(blue + f"Surname: {logged_user['surname']}")
        print(blue + f"Money: {green} {logged_user['money']}" + reset)
        print(blue + f"Email: {logged_user['email']}{reset}")
        print()

        action = input_quit_handle(
            "(1) Back to login Menu\n" "Enter your choice: "
        ).strip()
        if action == "1":
            return
        else:
            print(red + "Invalid choice. Please try again." + reset)


def delete_account(logged_user):
    clear()
    delete_confirmation = (
        input_quit_handle(
            red
            + f"Are you sure you want to delete Account '{logged_user['name']}'? (yes/no): "
            + reset
        )
        .strip()
        .lower()
    )
    if delete_confirmation == "yes":
        delete_user_and_inventory(logged_user["_id"])
        typing_effect(
            green
            + f"User '{logged_user['name']}' and their inventory deleted successfully!"
            + reset
        )
        return
    else:
        print(blue + "Delete action cancelled." + reset)
