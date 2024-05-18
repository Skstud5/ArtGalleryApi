import uvicorn
from fastapi import FastAPI
from api import user_router, paint_router, exposition_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(paint_router, prefix="/paintings", tags=["paintings"])
app.include_router(exposition_router, prefix="/expositions", tags=["expositions"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

uvicorn.run(app)
