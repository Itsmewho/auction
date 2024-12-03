# Log in menu
from utils.helpers import green, reset, input_quit_handle, clear, handle_quit


# Testing for now :
def menu_user_login(logged_user):

    while True:
        action = input_quit_handle(
            green + f"What do you want to do? \n"
            "(1) quit\n"
            "(2) quit with handle\n"
            "(3) goback\n"
            "Enter your choice: "
        ).strip()

        if action == "1":
            clear()
        elif action == "2":
            clear()
            handle_quit()
        elif action == "3":
            clear()
            break
