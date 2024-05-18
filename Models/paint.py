# Этот файл содержит определения схем Pydantic для
# валидации данных и передачи данных
# между клиентом и сервером.
from typing import Optional

from pydantic import BaseModel


class PaintCreate(BaseModel):
    title: str
    description: str
    uploaded_by: str
    image: str


class PaintUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    uploaded_by: Optional[str]
    image: Optional[str]


class PaintResponse(BaseModel):
    id: str
    title: str
    description: str
    uploaded_by: str
    image: str

    class Config:
        from_attributes = True

