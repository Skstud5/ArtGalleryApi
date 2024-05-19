from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from data_base.database import get_db
from models import ExpositionCreate, ExpositionResponse, ExpositionUpdate
from utils import serialize_model

router = APIRouter()


@router.get("/{id}", summary="Получить выставку по идентификатору", response_model=ExpositionResponse)
async def get(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        item = await db.expositions.find_one({"_id": ObjectId(id)})
        return serialize_model(ExpositionResponse, item)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.get("", summary="Получить все выставки", response_model=List[ExpositionResponse])
async def get_all(db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        items = await db.expositions.find().to_list(1000)
        return [serialize_model(ExpositionResponse, item) for item in items]
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("", summary="Создать выставку", response_model=ExpositionResponse)
async def create(item: ExpositionCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        dump = item.model_dump()
        dump["paintings"] = []
        result = await db.expositions.insert_one(dump)
        created_item = await db.expositions.find_one({"_id": result.inserted_id})
        return serialize_model(ExpositionResponse, created_item)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.delete("/{id}", summary="Удалить выставку", response_model=str)
async def delete(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        result = await db.expositions.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return "ok"
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.patch("/{id}", summary="Изменить данные о выставке", response_model=ExpositionResponse)
async def update(id: str, item: ExpositionUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        if not (item.uploaded_by is None) and (await db.users.find_one({'_id': ObjectId(item.uploaded_by)}) is None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого пользователя нет")
        dump = student = {
        k: v for k, v in item.model_dump(by_alias=True).items() if v is not None
    }
        print(dump)
        updated_item = await db.expositions.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dump},
            return_document=ReturnDocument.AFTER,
        )
        if updated_item is None:
            raise HTTPException(status_code=404, detail="Такой выставки нет")
        return serialize_model(ExpositionResponse, updated_item)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("/add_painting/{exposition_id}/{paint_id}", summary="Добавить картину", response_model=ExpositionResponse)
async def add_painting(exposition_id: str, paint_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        item = await db.expositions.find_one({"_id": ObjectId(exposition_id)})
        if item is None:
            raise HTTPException(status_code=404, detail="Такой выставки нет")
        if await db.paint.find_one({"_id": ObjectId(paint_id)}) is None:
            raise HTTPException(status_code=404, detail="Такой картины нет")
        item["paintings"].append(paint_id)
        updated_item = await db.expositions.find_one_and_update(
            {"_id": ObjectId(exposition_id)},
            {'$set': {"paintings": item["paintings"]}},
            return_document=ReturnDocument.AFTER,
        )
        return serialize_model(ExpositionResponse, updated_item)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException с кодом состояния 500
        error_message = f"An error occurred: {str(e)}"
        # print(error_message)  # Можно записать ошибку в логи для дальнейшего анализа
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
