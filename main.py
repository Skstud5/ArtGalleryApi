import uvicorn
from fastapi import FastAPI
from api import user_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

uvicorn.run(app)
