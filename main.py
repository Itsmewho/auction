# Main loop
from utils.helpers import *
from utils.register import validation_field


def main():

    # Checking functions remove later
    # Valid email
    print(validation_field("email", "test@example.com"))  # Output: True

    # Invalid email
    print(validation_field("email", "invalid-email"))  # Output: Invalid email address

    # Valid name
    print(validation_field("name", "John"))  # Output: True

    # Unknown field
    print(
        validation_field("unknown_field", "value")
    )  # Output: Unknown field: unknown_field


if __name__ == "__main__":
    main()
