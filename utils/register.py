# Register users
import os, re
import bcrypt
from db.db_operations import read_db
from models.all_models import RegisterModel
from pydantic import ValidationError, BaseModel
from utils.helpers import green, red, blue, reset, clear, input_quit_handle


# Check if fields are corresponding with model:
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


# Checking user input using the input_quit_handle
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


# Checking user existence
def check_user_exists(name):

    name = name.strip()
    existing_user = read_db("users", {"name": name})
    return len(existing_user) > 0
