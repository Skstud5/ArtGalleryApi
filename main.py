import uvicorn
from fastapi import FastAPI
from routers.routers import router as api_router

app = FastAPI()

app.include_router(api_router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

uvicorn.run(app)
