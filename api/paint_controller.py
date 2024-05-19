from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from data_base.database import get_db
from models import PaintCreate, PaintResponse, PaintUpdate
from utils import serialize_model

from logger.logger import log_error

router = APIRouter()


@router.get("/{id}", summary="Получить картину по идентификатору", response_model=PaintResponse)
async def get(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        item = await db.paint.find_one({"_id": ObjectId(id)})
        return serialize_model(PaintResponse, item)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException
        error_message = f"An error occurred: {str(e)}"
        log_error(f"Произошла ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.get("", summary="Получить все картины", response_model=List[PaintResponse])
async def get_all(db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        items = await db.paint.find().to_list(1000)
        return [serialize_model(PaintResponse, item) for item in items]
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException
        error_message = f"An error occurred: {str(e)}"
        log_error(f"Произошла ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("", summary="Создать картину", response_model=PaintResponse)
async def create(item: PaintCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        if await db.users.find_one({'_id': ObjectId(item.uploaded_by)}) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого пользователя нет")
        dump = item.model_dump()
        result = await db.paint.insert_one(dump)
        created_item = await db.paint.find_one({"_id": result.inserted_id})
        return serialize_model(PaintResponse, created_item)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException
        error_message = f"An error occurred: {str(e)}"
        log_error(f"Произошла ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.delete("/{id}", summary="Удалить картину", response_model=str)
async def delete(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        result = await db.paint.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return "ok"
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException
        error_message = f"An error occurred: {str(e)}"
        log_error(f"Произошла ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.patch("/{id}", summary="Изменить данные о картине", response_model=PaintResponse)
async def update(id: str, item: PaintUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        if not (item.uploaded_by is None) and (await db.users.find_one({'_id': ObjectId(item.uploaded_by)}) is None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого пользователя нет")
        dump = student = {
        k: v for k, v in item.model_dump(by_alias=True).items() if v is not None
    }
        print(dump)
        updated_item = await db.paint.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dump},
            return_document=ReturnDocument.AFTER,
        )
        if updated_item is None:
            raise HTTPException(status_code=404, detail="Такой картины нет")
        return serialize_model(PaintResponse, updated_item)
    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке и возвращаем HTTPException
        error_message = f"An error occurred: {str(e)}"
        log_error(f"Произошла ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
