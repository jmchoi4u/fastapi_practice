
from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter
from typing import Annotated, Optional
from sqlmodel import select

# 내부 모듈 임포트
from ..database import engine, get_session
from ..models import (
    User, UserPublic, UserCreate
)
from .. import utilities  # 해시 함수 등 사용 예정


router = APIRouter(
    prefix="/users",
    tags=['user']
)

# === USERS ===
@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate, session=Depends(get_session)):
    hashed_password = utilities.hash(user.password)
    user.password = hashed_password
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/me")
def read_users_me(current_user: User = Depends(utilities.get_current_user)):
    return current_user

@router.get("/{user_nickname}", response_model=UserPublic, )
def get_user(user_nickname: str, session=Depends(get_session)):
    found_user = session.exec(
        select(User).where(User.nickname == user_nickname)
    ).first()
    if not found_user:
        raise HTTPException(status_code=404, detail=f"User '{user_nickname}' not found")
    return found_user
