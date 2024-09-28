from pydantic import BaseModel, Field, EmailStr
from .models import RoleEnum


class UserBase(BaseModel):
    username:str = Field(max_length=22, min_length=3)
    email:EmailStr = Field()
    password:str = Field(max_length=72, min_length=8)
    role:RoleEnum = Field(default=RoleEnum.normal)
    isActive:bool = Field(default=True)

class UserIn(BaseModel):
    username:str = Field(max_length=22, min_length=3)
    email:EmailStr = Field()
    password:str = Field(max_length=72, min_length=8)

class UserOut(BaseModel):
    id:int
    username:str
    role:str


class PostBase(BaseModel):
   title:str
   content:str

class CommentBase(BaseModel):
    content: str
    postId:int = Field(gt=0)
