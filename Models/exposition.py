# Этот файл содержит определения схем Pydantic для
# валидации данных и передачи данных
# между клиентом и сервером.
import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class ExpositionCreate(BaseModel):
    name: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime


class ExpositionUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]


class ExpositionResponse(BaseModel):
    id: str
    name: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    paintings: Optional[List[str]] = Field(default=None)
    model_config = ConfigDict(from_attributes=True)