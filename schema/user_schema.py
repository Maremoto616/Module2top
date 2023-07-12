from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: Optional [str]
    name: str
    username: str
    userpassw: str

class DataUser(BaseModel):
    username: str
    userpassw: str