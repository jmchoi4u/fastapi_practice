# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Annotated, Optional
from fastapi.concurrency import asynccontextmanager
from sqlmodel import select
from datetime import datetime

# 내부 모듈 임포트
from .database import engine, get_session
from .models import (
    Post, PostPublic, PostCreate, PostUpdate,
    User, UserPublic, UserCreate
)
from . import utilities  # 해시 함수 등 사용 예정
from .routers import post,user,auth
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # 여기서 create_all
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    
    
app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

    





