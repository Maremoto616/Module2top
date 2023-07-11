from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED
from schema.user_schema import UserSchema
from config.db import engine
from model.users import users
from werkzeug.security import generate_password_hash , check_password_hash
from typing import List

user = APIRouter()

@user.get("/")
def root():
    return {"message": "Hi I am FastAPI with a router"} 

@user.get("/api/user", response_model=List[UserSchema])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        return result

@user.post("/api/user", status_code= HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn: #With se asegura que la conección se cierre apropiadamente
        new_user = data_user.dict()
        new_user["userpassw"] = generate_password_hash(data_user.userpassw,"pbkdf2:sha256:30", 30)

        conn.execute(users.insert().values(new_user))
        conn.commit()
        return Response(status_code=HTTP_201_CREATED)
    

@user.put("/api/user")
def update_user():
    pass