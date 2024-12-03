from utils.helpers import green, reset, input_quit_handle, clear, handle_quit


def menu_admin_login():
    # Testing
    while True:
        action = input_quit_handle(
            green + f"What do you want to do? \n"
            "(1) quit\n"
            "(2) quit without handle\n"
            "(3) logout\n"
            "Enter your choice admin: "
        ).strip()

        if action == "1":
            clear()
            break
        elif action == "2":
            clear()
            handle_quit()
            break
        elif action == "3":
            clear()
            return
