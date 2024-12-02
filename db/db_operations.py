# CRUD operations for universial use.
# Improved by GPT. Will use in the future, if proven usefull.

import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.collection import Collection
from utils.helpers import green, red, blue, reset


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DBNAME = os.getenv("MONGO_DBNAME")

# Collections call here for using elsewhere

MONGO_ADMIN = os.getenv("MONGO_ADMIN")
MONGO_USERS = os.getenv("MONGO_USERS")
MONGO_AUCTION = os.getenv("MONGO_AUCTION")
MONGO_INVENTORY = os.getenv("MONGO_INVENTORY")


client = MongoClient(MONGO_URI)
db = client[MONGO_DBNAME]


def create_db(collection_name: str, data: dict):

    try:
        collection: Collection = db[collection_name]
        collection.insert_one(data)
        logger.info(green + f"Document inserted into {collection_name}", reset)
    except PyMongoError as e:
        logger.info(red + f"Error insterting document: {e}", reset)
    except Exception as e:
        logger.info(red + f"Unexpected error insterting document: {e}", reset)


def read_db(
    collection_name: str, query: dict = None, limit: int = 0, sort_by: tuple = None
) -> list:

    # Cool '->', is used for function annotations: (https://peps.python.org/pep-3107/)

    try:
        if query is None:
            query = {}

        collection: Collection = db[collection_name]

        cursor = collection.find(query)
        if sort_by:
            cursor = cursor.sort(sort_by)
        if limit:
            cursor = cursor.limit(limit)

        result = list(cursor)
        logger.info(
            green + f"Read {len(result)} documents from {collection_name}", reset
        )
        return result
    except PyMongoError as e:
        logger.error(red + f"Error reading data from {collection_name}: {e}", reset)
        return []
    except Exception as e:
        logger.error(
            red + f"Unexpected error reading data from {collection_name}: {e}", reset
        )
        return []


def update_db(
    collection_name: str, query: dict, update_data: dict, multiple: bool = False
):

    try:
        collection: Collection = db[collection_name]

        if "$set" not in update_data:
            update_data = {"$set": update_data}

        if multiple:
            result = collection.update_many(query, update_data)
        else:
            result = collection.update_one(query, update_data)

        if result.modified_count > 0:
            logger.info(green + f"Document(s) updated in {collection_name}", reset)
        else:
            logger.info(
                blue + f"No documents matched for update in {collection_name}", reset
            )
    except PyMongoError as e:
        logger.error(red + f"Error updating data in {collection_name}: {e}", reset)
    except Exception as e:
        logger.error(
            red + f"Unexpected error updating data in {collection_name}: {e}", reset
        )


def delete_db(collection_name: str, query: dict, multiple: bool = False):

    try:
        collection: Collection = db[collection_name]

        if multiple:
            result = collection.delete_many(query)
        else:
            result = collection.delete_one(query)

        if result.deleted_count > 0:
            logger.info(green + f"Deleted document(s) from {collection_name}", reset)
        else:
            logger.info(
                blue + f"No documents matched for deletion in {collection_name}", reset
            )
    except PyMongoError as e:
        logger.error(red + f"Error deleting document in {collection_name}: {e}", reset)
    except Exception as e:
        logger.error(
            red + f"Unexpected error deleting document in {collection_name}: {e}", reset
        )
