from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from data_base.database import get_db
from models import UserCreate, UserResponse, UserUpdate
from security.security import get_password_hash
from utils import serialize_model

router = APIRouter()


@router.get("/{id}", response_description="Получить пользователя по идентификатору", response_model=UserResponse)
async def get(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        item = await db.users.find_one({"_id": ObjectId(id)})
        return serialize_model(UserResponse, item)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.get("", response_description="Получить всех пользователей", response_model=List[UserResponse])
async def get_all(db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        items = await db.users.find().to_list(1000)
        return [serialize_model(UserResponse, item) for item in items]
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("", response_description="Создать пользователя", response_model=UserResponse)
async def create(item: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        item.password = get_password_hash(item.password)
        dump = item.model_dump()
        result = await db.users.insert_one(dump)
        created_item = await db.users.find_one({"_id": result.inserted_id})
        return serialize_model(UserResponse, created_item)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.delete("/{id}", response_description="Удалить пользователя", response_model=str)
async def delete(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        result = await db.users.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return "ok"
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.patch("/{id}", response_description="Изменить данные о пользователе", response_model=UserResponse)
async def update(id: str, item: UserUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        dump = student = {
        k: v for k, v in item.model_dump(by_alias=True).items() if v is not None
    }
        print(dump)
        updated_item = await db.users.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dump},
            return_document=ReturnDocument.AFTER,
        )
        if updated_item is None:
            raise HTTPException(status_code=404, detail="Такого пользователя нет")
        return serialize_model(UserResponse, updated_item)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
