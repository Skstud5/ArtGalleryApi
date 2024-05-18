# models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from data_base.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    images = relationship("Image", back_populates="owner")
    comments = relationship("Comment", back_populates="author")


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    url = Column(String)
    uploaded_by = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="images")
    comments = relationship("Comment", back_populates="image")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    image_id = Column(Integer, ForeignKey('images.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    image = relationship("Image", back_populates="comments")
    author = relationship("User", back_populates="comments")
