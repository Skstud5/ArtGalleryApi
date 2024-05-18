from fastapi import FastAPI
from data_base.database import engine, Base
from routers.routers import router as api_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api_router)
