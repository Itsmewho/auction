# Log in menu
from utils.auction import auction
from utils.admin_menu import delete_user_and_inventory
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
            clear()
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
    print(f"Viewing inventory for {logged_user['name']}...")


def sell_items(logged_user):
    print(f"{logged_user['name']} is selling items...")


def view_account_details(logged_user):
    print(f"Viewing account details for {logged_user['name']}...")


def delete_account(logged_user):
    clear()
    delete_confirmation = (
        input_quit_handle(
            red
            + f"Are you sure you want to delete user '{logged_user['name']}'? (yes/no): "
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
