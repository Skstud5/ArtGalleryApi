# Этот файл содержит определения схем Pydantic для
# валидации данных и передачи данных
# между клиентом и сервером.
import datetime
from typing import Optional, List

from pydantic import BaseModel


class ExpositionCreate(BaseModel):
    name: str
    description: str
    start_date: datetime.date
    end_date: datetime.date


class ExpositionUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]


class ExpositionResponse(BaseModel):
    id: str
    name: str
    description: str
    start_date: datetime.date
    end_date: datetime.date
    paintings: List[str]

    class Config:
        from_attributes = True

