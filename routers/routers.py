from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.database import Database as MongoDBDatabase
from data_base.database import get_db
from models.schemas import UserCreate, UserResponse
from security.security import create_access_token, authenticate_user, get_password_hash

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: MongoDBDatabase = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password
    }
    inserted_user = db.users.insert_one(user_data)
    user_id = inserted_user.inserted_id
    user_data["_id"] = user_id
    return user_data


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: MongoDBDatabase = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
