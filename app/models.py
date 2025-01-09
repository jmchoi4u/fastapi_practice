# app/models.py
from datetime import datetime, timedelta
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel
# from sqlalchemy import TIMESTAMP  # 필요하면 import



# User Models
class UserBase(SQLModel):
    __tablename__ = "users"
    # nickname: str = Field(nullable=False, unique=True)

class User(UserBase, table=True):
    nickname: str = Field(nullable=False, unique=True)
    id: int = Field(primary_key=True, default=None)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    createtime_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta())
    # One-to-Many: 한 User가 여러 Post를 갖는다
    posts: List["Post"] = Relationship(back_populates="owner")

class UserPublic(UserBase):
    nickname: str
    id: int
    createtime_at: datetime
    
    

class UserCreate(UserBase):
    nickname : str
    email: EmailStr
    password: str
    
    
class UserLogin(UserBase):
    email : EmailStr
    password : str
    
    
#Token Model
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    


# Post Models
class PostBase(SQLModel):
    __tablename__ = "posts"  # SQLModel에서는 이렇게 지정할 수도 있음
    title: str
    content: str

class Post(PostBase, table=True):
    id: int = Field(primary_key=True, default=None)
    secret_name: Optional[str] = None
    published: bool = Field(default=True)
    createtime_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta()
    )
    owner_id : Optional[int] = Field(default=None, foreign_key="users.id", ondelete="CASCADE")
    # Many-to-One: 여러 Post가 한 User를 가리킴
    # 타입 힌트를 "User" (문자열)로 하여 forward reference
    owner: "User" = Relationship(back_populates="posts") #TODO back_populates

class PostPublic(PostBase):
    id: int
    published: bool
    createtime_at: datetime
    owner_id : int
    owner : "UserPublic"
    

class PostCreate(PostBase):
    secret_name: str

class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    secret_name: Optional[str] = None
    

#Vote
class VoteBase(SQLModel):
    __tablename__ = "votes"


class Vote(VoteBase, table = True):
    votes_id: int = Field(foreign_key="users.id", ondelete="CASCADE", primary_key=True)
    posts_id: int = Field(foreign_key="posts.id", ondelete="CASCADE", primary_key=True)