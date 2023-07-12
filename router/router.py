from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from schema.user_schema import UserSchema, DataUser
from config.db import engine
from model.users import users
from werkzeug.security import generate_password_hash , check_password_hash
from typing import List


user = APIRouter()

@user.get("/")
def root():
    return {"message": "Hi I am FastAPI with a router"} 

@user.get("/api/user")
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        return result
    
@user.get("/api/user/{user_id}")
def get_user_by_id(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).fetchall()
        user_list = [dict(row) for row in result]
        return user_list

@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        new_user["userpassw"] = generate_password_hash(data_user.userpassw, "pbkdf2:sha256:30", 30)

        conn.execute(users.insert().values(new_user))

        # Obtener la lista actualizada de usuarios
        result = conn.execute(users.select()).fetchall()
        user_list = [dict(row) for row in result]

        return user_list
    
@user.post("/api/user/login")
def user_login(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).first()

        if result is not None:
            check_passw = check_password_hash(result[3], data_user.userpassw)

            if check_passw:
                return {
                    "status":200,
                    "message": "Access success"
                }

        return {
                "status":HTTP_401_UNAUTHORIZED,
                "message": "Access denied"
                }
    


@user.put("/api/user/{user_id}")
def update_user(data_update: UserSchema, user_id: str):
    with engine.connect() as conn:
        encryp_passw = generate_password_hash(data_update.userpassw, "pbkdf2:sha256:30", 30)

        conn.execute(
            users.update()
            .values(
                name=data_update.name,
                username=data_update.username,
                userpassw=encryp_passw
            )
            .where(users.c.id == user_id)
        )

        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        return result

@user.delete("/api/user/{user_id}")
def delete_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        if result:
            conn.execute(users.delete().where(users.c.id == user_id))
            return Response(status_code=HTTP_204_NO_CONTENT)
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)        
        

'''
La API creada tiene:

Una ruta base
Una ruta para poder solicitar usuarios 
Una ruta para crear usuarios
Una ruta para filtrar a un usuario 
Una ruta para eliminar un usuario 
Una ruta para hacer el login del usuario 
Una ruta de actualización del usuario 


'''