# Main loop
from utils.helpers import *
from utils.register import main_register
from utils.login import login
from utils.admin_menu import menu_admin_login
from utils.login_menu import menu_user_login


def main():
    print(blue + "Welcome to the Auction System!" + reset)

    while True:
        action = input_quit_handle(
            "Do you want to login or register? (login/register): "
        ).lower()
        clear()

        if action in ["register", "r", "reg"]:
            clear()
            main_register()
            continue

        elif action in ["login", "log", "l"]:
            logged_user = login()

            if logged_user is None:
                continue

            if logged_user["role"] == "admin":
                clear()

                menu_admin_login()
            else:
                clear()
                menu_user_login(logged_user)
            continue
        else:
            print(red + "Invalid input. Please enter 'login' or 'register'." + reset)


if __name__ == "__main__":
    main()
