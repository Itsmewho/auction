# Register users
import bcrypt
from db.db_operations import read_db, create_db
from models.all_models import RegisterModel
from pydantic import ValidationError, BaseModel
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


def validation_field(field_name: str, value: str, model=RegisterModel):

    if field_name not in model.model_fields:
        return blue + f"Unknown field: {field_name}{reset}"

    field_type = model.model_fields[field_name].annotation

    class TempModel(BaseModel):
        __annotations__ = {field_name: field_type}

    try:
        TempModel(**{field_name: value})
        return True
    except ValidationError as e:
        error_message = e.errors()[0]["msg"]
        return red + f"Validation error for '{field_name}': {error_message}{reset}"


def validation_input(prompt, field_name, min_length=None, model=RegisterModel):
    while True:
        user_input = input_quit_handle(prompt).strip()

        if min_length and len(user_input) < min_length:
            print(
                red
                + f"{field_name} must be at least {min_length} characters long. Please try again.{reset}"
            )
            continue

        validation = validation_field(field_name, user_input, model)
        if validation is True:
            return user_input
        else:
            input_quit_handle(red + f"Invalid: {field_name} : {validation}{reset}")


def check_user_exists(email):

    email = email.strip()
    existing_user = read_db("users", {"email": email})
    return len(existing_user) > 0


def encrypt_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def check_password(stored_password, entered_password):
    return bcrypt.checkpw(
        entered_password.encode("utf-8"), stored_password.encode("utf-8")
    )


def main_register():
    while True:
        print(green + "Register a New User" + reset)

        name = validation_input("Enter your first name: ", "name", min_length=3).title()

        surname = validation_input(
            "Enter your surname: ", "surname", min_length=3
        ).title()

        email = validation_input("Enter your email: ", "email").lower()

        if check_user_exists(email):
            clear()
            typing_effect(
                red + f"A user with the email '{email}' already exists.{reset}"
            )
            response = input_quit_handle("Do you want to retry? (y/n): ").lower()
            if response == "y":
                continue
            else:
                typing_effect(red + "Returning to main menu...{reset}")
                return

        break

    while True:
        secure_password = input_masking(
            green + "Enter a password (min length is 4): ", "secure_password"
        )
        if len(secure_password) < 4:
            typing_effect(red + "Password must be at least 4 characters long!{reset}")
            continue

        confirm_pass = input_masking(green + "Confirm password: ")
        if secure_password != confirm_pass:
            typing_effect(red + "Passwords do not match! Try again.{reset}")
            continue

        break

    try:
        user_data = RegisterModel(
            name=name,
            surname=surname,
            email=email,
            secure_password=secure_password,
        )
        hashed_password = encrypt_password(user_data.secure_password)
        user_data_dict = user_data.model_dump()
        user_data_dict["secure_password"] = hashed_password.decode("utf-8")
        user_data_dict["money"] = 5000

        create_db("users", user_data_dict)
        clear()
        typing_effect(green + f"User '{name}' registered successfully! 👌 {reset}")
    except ValidationError as e:
        typing_effect(red + f"Error: {e}{reset}")
