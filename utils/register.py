# Register users
import os, re
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


def validation_input(prompt, field_type, min_length=None):

    while True:
        user_input = input_quit_handle(prompt).title()

        if min_length and len(user_input) < min_length:
            print(
                red
                + f"{field_type} must be at least {min_length} characters long. Please try again{reset}"
            )
            continue

        validation = validation_field(field_type, user_input)
        if validation is True:
            return user_input
        input_quit_handle(red + f"Invalid: {field_type} : {validation}{reset}")


def check_user_exists(name):

    name = name.strip()
    existing_user = read_db("users", {"name": name})
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

        clear()
        print(green + "Register a New User" + reset)

        name = validation_input("Enter you first name: ", "name").title()
        surname = validation_input("Enter you surname: ", "surname").title()
        email = validation_field("Enter your email: ", "email").lower()

        validation = validation_field("email", email)
        if validation is not True:
            typing_effect(red + f"Invalid email: {validation}{reset}")
            continue

        if check_user_exists(name):
            clear()
            typing_effect(
                red + f"A user with the {name} and {surname} already exist{reset}"
            )

            response = input_quit_handle("Do you want to retry? (y/n) : ").lower()
            if response == "y":
                continue
            else:
                typing_effect(red + f"Invalid response. Please enter: (y/n).")
        else:
            return

        break

    while True:

        clear()
        secure_password = input_masking(
            green + f"Enter a password (min length is 4):", "secure_password"
        )
        if len(secure_password) < 4:
            typing_effect(red + f"Invalid password must be 4 characters long!{reset}")
            continue

        confirm_pass = input_masking(green + f"Confirm password:")
        if secure_password != confirm_pass:
            typing_effect(red + f"Passwords do not match!. Try again{reset}")
            continue

        break

    # Check everything again.
    try:
        user_data = RegisterModel(
            name=name, surname=surname, email=email, secure_password=secure_password
        )
        hashed_password = encrypt_password(user_data.secure_password)
        user_data_dict = user_data.model_dump()
        user_data_dict["secure_password"] = hashed_password.decode("utf-8")

        create_db("users", user_data_dict)
        typing_effect(green + f"User: {name}, registerd successfully!👌 {reset}")
    except ValueError as e:
        typing_effect(red + f"Error: {e}")
