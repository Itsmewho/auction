from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AuctionItem(BaseModel):
    item: str
    price: float = Field(gt=0, description="Price must be greater than 0.")
