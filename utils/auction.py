import time
import random
from db.db_operations import read_db, insert_db, delete_db, update_db
from utils.helpers import (
    typing_effect,
    clear,
    input_quit_handle,
    red,
    green,
    reset,
    sleep,
)


def get_random_items():
    auction_items = read_db("auction_items")
    if len(auction_items) < 3:
        typing_effect(red + "Not enough items for an auction!" + reset)
        return []
    return random.sample(auction_items, 3)


def auction(logged_user):
    # Main logic
    typing_effect(
        green + f"Welcome to the auction house, {logged_user['name']}!😇" + reset
    )
    sleep()

    while True:
        clear()
        response = (
            input_quit_handle(green + "Do you want to buy an item? (yes/no): " + reset)
            .strip()
            .lower()
        )
        if response in {"y", "yes"}:
            pass  # Proceed to show auction items
        elif response in {"n", "no"}:
            return
        else:
            typing_effect(red + "Invalid input. Please try again." + reset)
            continue

        items = get_random_items()
        if not items:
            typing_effect(red + "No items available for auction." + reset)
            return

        print(green + "Today's auction items:" + reset)
        for idx, item in enumerate(items, start=1):
            print(f"({idx}) {item['item']} - Starting price: {item['price']}")

        print(f"({len(items) + 1}) Go back to the previous menu")

        choice = input_quit_handle(
            "Enter the number of the item you want to bid on, or go back: "
        ).strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(items):
                selected_item = items[choice - 1]
                run_auction(logged_user, selected_item)
            elif choice == len(items) + 1:
                return
            else:
                print(red + "Invalid choice. Please try again." + reset)
        else:
            print(red + "Invalid input. Please enter a valid number." + reset)


def run_auction(logged_user, item):
    clear()
    auction_time = random.randint(1, 3)
    end_time = time.time() + auction_time * 60
    highest_bid = item["price"]
    computer_budget = random.uniform(0.5, 1.5) * read_user_money(logged_user["_id"])

    typing_effect(
        green
        + f"Starting Auction for {item['item']}! Auction ends in {auction_time} minutes."
        + reset
    )
    while time.time() < end_time:
        clear()
        print(green + f"Current Highest Bid: {highest_bid}" + reset)
        bid = input_quit_handle(
            green + f"Enter your bid (or type 'leave' to exit): "
        ).strip()

        if bid.lower() in {"l", "leave"}:
            typing_effect(red + "You left the auction." + reset)
            return
        if not bid.isdigit() or int(bid) <= highest_bid:
            typing_effect(
                red + "Invalid bid. Must be higher than the current bid." + reset
            )
            continue

        bid = int(bid)
        if not has_money(logged_user["_id"], bid):
            typing_effect(
                red + "You don't have enough money to place this bid." + reset
            )
            continue

        highest_bid = bid

        if computer_budget > highest_bid:
            computer_bid = random.randint(highest_bid + 1, int(computer_budget))
            highest_bid = computer_bid
            print(green + f"Unknown bidder placed a bid of {computer_bid}!" + reset)
        else:
            print(green + "Unknown bidder can't place any higher bids!" + reset)
            break

    if highest_bid == bid:
        print(
            green + f"Congratulations! You won the auction for {item['item']}!" + reset
        )
        update_user_money(logged_user["_id"], -highest_bid)
        add_item_to_inventory(logged_user["_id"], item)
        delete_db("auction_items", {"_id": item["_id"]})
    else:
        print(red + f"You lost the auction. Item was sold for {highest_bid}." + reset)


def read_user_money(user_id):
    user = read_db("users", {"_id": user_id})
    return user[0]["money"] if user else 0


def has_money(user_id, amount):
    return read_user_money(user_id) >= amount


def update_user_money(user_id, amount_change):
    update_db("users", {"_id": user_id}, {"$inc": {"money": amount_change}})


def add_item_to_inventory(user_id, item):
    new_item = {
        "user_id": user_id,
        "item": item["item"],
        "sellprice": float(item["price"]),
    }
    insert_db("inventory", new_item)
    print(green + f"Item '{item['item']}' added successfully!" + reset)
