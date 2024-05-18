# Этот файл содержит определения схем Pydantic для
# валидации данных и передачи данных
# между клиентом и сервером.
from pydantic import BaseModel
from typing import List, Optional


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


class ImageCreate(BaseModel):
    title: str
    description: str
    url: str


class ImageResponse(BaseModel):
    id: int
    title: str
    description: str
    url: str
    uploaded_by: int
    comments: Optional[List['CommentResponse']] = []

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str
    image_id: int


class CommentResponse(BaseModel):
    id: int
    content: str
    image_id: int
    user_id: int

    class Config:
        orm_mode = True
