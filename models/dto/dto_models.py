from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
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
    id: str
    title: str
    description: str
    url: str
    uploaded_by: str

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str
    image_id: str
