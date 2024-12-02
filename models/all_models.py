from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AuctionItem(BaseModel):
    item: str
    price: float = Field(gt=0, description="Price must be greater than 0.")


class InventoryItem(BaseModel):
    item: str
    sellprice: float = Field(gt=0, description="Sell price must be greater than 0.")


class register(BaseModel):
    name: str
    surname: str
    email: EmailStr
    secure_password: str
    repeat_password: str


class User(BaseModel):
    name: str
    surname: str
    email: EmailStr
    secure_password: str
