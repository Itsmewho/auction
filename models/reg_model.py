from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class register(BaseModel):
    name: str
    surname: str
    email: EmailStr
    secure_password: str
    repeat_password: str
