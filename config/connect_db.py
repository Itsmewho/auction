# Checking the connection.
import os
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DBNAME = os.getenv("MONGO_DBNAME")

# Collections.
MONGO_ADMIN = os.getenv("MONGO_ADMIN")
MONGO_USERS = os.getenv("MONGO_USERS")
MONGO_AUCTION = os.getenv("MONGO_AUCTION")
MONGO_INVENTORY = os.getenv("MONGO_INVENTORY")


# Checking collections.
def get_collection(collection_name):
    return db[collection_name]


admin_collection = get_collection(MONGO_ADMIN)
users_collection = get_collection(MONGO_USERS)
auction_collection = get_collection(MONGO_AUCTION)
inventory_collection = get_collection(MONGO_INVENTORY)


# Connection
client = MongoClient(MONGO_URI)
db = client[MONGO_DBNAME]
