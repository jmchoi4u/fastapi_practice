from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter, status
from typing import Annotated, Optional
import fastapi
from sqlmodel import select
from datetime import datetime

# 내부 모듈 임포트
from ..database import engine, get_session
from ..models import (
    Post, PostPublic, PostCreate, PostUpdate,
    User, UserPublic, UserCreate
)
from .. import utilities  # 해시 함수 등 사용 예정


router = APIRouter(
    prefix="/posts",
    tags=['post']
)



# === POSTS ===
@router.post("/", response_model=PostPublic)
def create_post(post: PostCreate, session=Depends(get_session), current_user: User = Depends(utilities.get_current_user)):
    # db_post = Post.model_validate(post)
    db_post = Post(owner_id=current_user.id, **post.model_dump())
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.get("/", response_model=list[PostPublic])
def read_myself_posts(
    session=Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    current_user: User = Depends(utilities.get_current_user),
    search : Optional[str] = "",
):
    posts = session.exec(
        select(Post).offset(offset).limit(limit).where(Post.owner_id == current_user.id)
    ).all()
    return posts

@router.get("/all", response_model=list[PostPublic])
def read_all_posts(
    session=Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    search : Optional[str] = "",
):
    posts = session.exec(
        select(Post).filter(Post.title.contains(search)).offset(offset).limit(limit)
    ).all()
    return posts


@router.get("/{post_id}", response_model=PostPublic)
def read_post(post_id: int, session=Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.patch("/{post_id}", response_model=PostPublic)
def update_post(post_id: int, post: PostUpdate,
                session=Depends(get_session),
                current_user: User = Depends(utilities.get_current_user)  
                # 인증 필수
                ):
    """
    글 수정(인증 필요).
    """
    post_db = session.get(Post, post_id)
    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post_db.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_data = post.model_dump(exclude_unset=True)
    post_db.sqlmodel_update(post_data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db

@router.delete("/{post_id}")
def delete_post(post_id: int,
                session=Depends(get_session),
                current_user: User = Depends(utilities.get_current_user)  
            ):
    """
    글 삭제(인증 필요).
    """
    post = session.get(Post, post_id)
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    session.delete(post)
    session.commit()
    return {"ok": True}