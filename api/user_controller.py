# from pymongo.database import Database as MongoDBDatabase
# from fastapi.security import OAuth2PasswordRequestForm
from re import T
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from data_base.database import get_db
from schemas import UserCreate, UserResponse
from security.security import get_password_hash
from utils import serialize_model

router = APIRouter()


@router.get("/{id}", response_model=UserResponse)
async def get(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        user = await db.users.find_one({"_id": ObjectId(id)})
        return serialize_model(UserResponse, user)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.get("", response_model=List[UserResponse])
async def get_all(db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        users = await db.users.find().to_list(1000)
        return [serialize_model(UserResponse, item) for item in users]
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("", response_model=UserResponse)
async def create(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        hashed_password = get_password_hash(user.password)
        user_data = {
            "username": user.username,
            "email": user.email,
            "hashed_password": hashed_password
        }
        inserted_user = await db.users.insert_one(user_data)

        user_id = str(inserted_user.inserted_id)
        user_data["id"] = user_id

        return user_data
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)

