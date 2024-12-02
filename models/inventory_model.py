from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class InventoryItem(BaseModel):
    item: str
    sellprice: float = Field(gt=0, description="Sell price must be greater than 0.")
