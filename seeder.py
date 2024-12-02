# For checking db and basic operrations
import json
from pydantic import BaseModel, ValidationError
from config.connect_db import (
    admin_collection,
    users_collection,
    auction_collection,
    inventory_collection,
)
from models.all_models import UserModel, RegisterModel, InventoryModel, AuctionModel
from db.db_operations import create_db
from utils.helpers import green, red, reset


def load_json(filepath: str) -> list:

    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(red + f"File not found: {filepath}{reset}")
        return None
    except json.JSONDecodeError as e:
        print(red + f"Error decoding JSON: {e}{reset}")
        return None


def seed_data(collection_name: str, data: list, model):

    for record in data:
        try:
            validated_record = model(**record).model_dump()
            create_db(collection_name, validated_record)
            print(
                green + f"Inserted into {collection_name} : {validated_record}{reset}"
            )
        except ValidationError as e:
            print(red + f"Validation Error: {e}{reset}")
        except Exception as e:
            print(red + f"Unexpected error: {e}{reset}")


def seeding():

    # Users
    user_data = load_json("data/users.json")
    seed_data("users", user_data, UserModel)

    # Auction Items
    auction_data = load_json("data/auction_items.json")
    seed_data("auction_items", auction_data, AuctionModel)

    # Inventory
    inventory_data = load_json("data/inventory.json")
    seed_data("inventory", inventory_data, InventoryModel)


if __name__ == "__main__":
    seeding()
