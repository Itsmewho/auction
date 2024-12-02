from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AuctionModel(BaseModel):
    item: str
    price: float = Field(gt=0, description="Price must be greater than 0.")


class InventoryModel(BaseModel):
    item: str
    sellprice: float = Field(gt=0, description="Sell price must be greater than 0.")


class RegisterModel(BaseModel):
    name: str = Field(..., min_length=3)
    surname: str = Field(..., min_length=3)
    email: EmailStr
    secure_password: str = Field(..., min_length=4)
    repeat_password: str = Field(..., min_length=4)


class UserModel(BaseModel):
    name: str
    surname: str
    email: EmailStr
    secure_password: str
