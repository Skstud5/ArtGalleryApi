from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from pymongo.database import Database as MongoDBDatabase
from data_base.database import get_db
from models.schemas import User
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Define oauth2_scheme as an instance of OAuth2PasswordBearer

# tokenUrl - это URL, на который клиент будет отправлять запросы для получения токена доступа.
# Когда клиент отправляет запрос на этот URL с учетными данными (имя пользователя и пароль) в теле запроса,
# сервер проверяет эти учетные данные и, если они корректны, выдает токен доступа.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# TODO Вынести в .ENV секретный ключ и алгоритм
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: MongoDBDatabase, username: str, password: str):
    user = db.users.find_one({"username": username})
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return User(**user)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: MongoDBDatabase = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.users.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return User(**user)
