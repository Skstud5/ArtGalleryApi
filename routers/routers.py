# from pymongo.database import Database as MongoDBDatabase
# from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from data_base.database import get_db
from models.schemas import UserCreate, UserResponse
from security.security import get_password_hash

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
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


# @router.post("/token")
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
#                            db: MongoDBDatabase = Depends(get_db)):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=400,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(data={"sub": user["username"]})
#     return {"access_token": access_token, "token_type": "bearer"}
