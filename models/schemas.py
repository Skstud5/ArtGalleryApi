# Этот файл содержит определения схем Pydantic для
# валидации данных и передачи данных
# между клиентом и сервером.
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True
