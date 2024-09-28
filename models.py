from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum as SQLAEnum
from sqlalchemy.orm import relationship
from .db import Base
from datetime import datetime
from enum import Enum


class RoleEnum(str,Enum):
    admin = "admin"
    normal = "normal"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(SQLAEnum(RoleEnum), nullable=False, default=RoleEnum.normal)
    isActive = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.now)
    authorId = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    createdAt = Column(DateTime, default=datetime.now)
    authorId= Column(Integer, ForeignKey("users.id"))
    postId = Column(Integer, ForeignKey("posts.id"))

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
