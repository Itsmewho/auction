from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    name: str
    surname: str
    email: EmailStr
    secure_password: str
