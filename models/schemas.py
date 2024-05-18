# Этот файл содержит определения схем Pydantic для
# валидации данных и передачи данных
# между клиентом и сервером.
from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    email: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    hashed_password: str

    class Config:
        from_attributes = True
