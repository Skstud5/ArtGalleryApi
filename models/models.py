from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(alias="_id")
    username: str
    email: str
    hashed_password: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "hashed_password": "hash123",
            }
        }