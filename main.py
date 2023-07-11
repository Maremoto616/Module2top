from fastapi import FastAPI
from router.router import user

app = FastAPI()

# http://127.0.0.1:8000


app.include_router(user)
