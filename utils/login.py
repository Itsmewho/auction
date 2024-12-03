# Login logic
from db.db_operations import read_db
from utils.register import check_password
from utils.helpers import (
    green,
    red,
    blue,
    reset,
    clear,
    input_quit_handle,
    input_masking,
    typing_effect,
)


def check_login(name: str, email: str, entered_password: str):

    try:
        name = name.strip().title()
        email = email.strip().lower()

        user = read_db("users", {"name": name, "email": email})

        if user:
            user = user[0]
            stored_password = user["secure_password"]

            # Validate password
            if check_password(stored_password, entered_password):
                return True, user
            return False, red + f"Incorrect password.{reset}"
        return False, red + f"User not found.{reset}"

    except Exception as e:
        return False, red + f"Error checking user: {e}{reset}"


def login():

    max_attempts = 3  # Limit login attempts
    attempts = 0

    while attempts < max_attempts:
        clear()
        print(blue + "Login to your account" + reset)

        name = input_quit_handle("Enter your name : ").title()

        # Kind of useless but it gets the main idea:
        admin_check = read_db("admin", {"name": name})
        print(f"Debug: Admin check result: {admin_check}")

        if admin_check and len(admin_check) > 0:
            admin = admin_check[0]
            print(green + f"Welcome, {name}! (Admin)" + reset)
            return {"role": "admin", **admin}

        email = input_quit_handle("Enter your email : ").title()
        password = input_masking(green + f"Enter your password:")

        valid, user = check_login(name, email, password)

        if valid:
            typing_effect(green + f"Login successfull!{reset}")
            return user
        else:
            print(red + f"Invalid combination!{reset}")

        attempts += 1
        if attempts < max_attempts:
            retry = input_quit_handle("Do you want to try again? (y/n): ").lower()
            if retry == "y":
                continue
            elif retry == "n":
                print(red + "Exiting login." + reset)
                return None
            else:
                print(red + "Invalid input. Please enter 'y' or 'n'." + reset)
        else:
            print(
                red + "Maximum login attempts exceeded. Please try again later." + reset
            )
