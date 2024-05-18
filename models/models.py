from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(alias="_id")
    username: str
    email: str
    hashed_password: str
    is_active: bool = True

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "hashed_password": "hash123",
                "is_active": True
            }
        }


class Image(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str
    url: str
    uploaded_by: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "Example Image",
                "description": "This is an example image",
                "url": "http://example.com/image.jpg",
                "uploaded_by": "60d8a09f365e0e1c50646707"
            }
        }


class Comment(BaseModel):
    id: str = Field(alias="_id")
    content: str
    image_id: str
    user_id: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "content": "This is a comment",
                "image_id": "60d8a09f365e0e1c50646707",
                "user_id": "60d8a09f365e0e1c50646708"
            }
        }
