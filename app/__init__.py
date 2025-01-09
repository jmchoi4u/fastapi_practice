
#참고: __init__.py는 “파이썬 패키지”로 인식하기 위해 종종 비어 있는 파일로 두기도 합니다.
#main.py를 최상위에 둬도 괜찮지만, 보통 app/ 폴더 안에 함께 두는 편이 많아요.

# from datetime import datetime, timedelta
# from typing import Annotated, Optional, Union

# from http import HTTPStatus
# from fastapi import Depends, FastAPI, HTTPException, Query, status
# from pydantic import EmailStr
# from sqlalchemy import TIMESTAMP
# from sqlmodel import Field, Session, SQLModel, create_engine, select 
# from . import utilities



# class PostBase(SQLModel):
#     __tablename__ = "posts"
    
#     title : str 
#     content : str

# class Post(PostBase, table = True):
#     id : int = Field(primary_key=True, default=None)
#     secret_name : str
#     published : bool = Field(default=True)
#     createtime_at : datetime = Field(default_factory = lambda: datetime.now() + timedelta() )
    
# class PostPublic(PostBase):
#     id : int
#     published : bool
#     createtime_at : datetime
    
# class PostCreate(PostBase):
#     secret_name : str
    
# class PostUpdate(PostBase):
#     title: Optional[str] = None
#     content: Optional[str] = None
#     secret_name: Optional[str] = None
    

# class UserBase(SQLModel):
#     __tablename__ = "users"

#     nickname : str = Field(nullable=False, unique=True,)

# class User(UserBase, table = True):
#     id : int = Field(primary_key=True, default=None)
#     email : str = Field(nullable=False, unique=True)
#     password : str = Field(nullable=False)
#     createtime_at : datetime = Field(default_factory = lambda: datetime.now() + timedelta() )
    
# class UserPublic(UserBase):
#     id : int
#     createtime_at : datetime

# class UserCreate(UserBase):
#     email : EmailStr
#     password : str


    
# # DB 접속 정보
# db_host = "localhost" # ex) ec2-123-123-123-123.ap-northeast-2.compute.amazonaws.com
# user = "postgres"
# password = "1234"

# engine = create_engine(f'postgresql://{user}:{password}@{db_host}/postgres')

# def create_db_and_tables(): #To create Table
#     SQLModel.metadata.create_all(engine)

# def get_session():
#     with Session(engine) as session:
#         yield session
        
# app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()
    
# @app.post("/posts", response_model = PostPublic)
# def create_post(post: PostCreate, session: Session = Depends(get_session)):
#     db_post = Post.model_validate(post)
#     session.add(db_post)
#     session.commit()
#     session.refresh(db_post)
#     return db_post

# @app.get("/posts", response_model = list[PostPublic])
# def read_posts(
#     session: Session = Depends(get_session),
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ):
#     posts = session.exec(select(Post).offset(offset).limit(limit)).all()
#     return posts

# @app.get("/posts/{post_id}", response_model = PostPublic)
# def read_post(post_id: int, session: Session = Depends(get_session)):
#     post = session.get(Post, post_id)
#     if not post:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     return post

# @app.patch("/posts/{post_id}", response_model = PostPublic)
# def update_post(post_id: int, post: PostUpdate, session: Session = Depends(get_session)):
#     post_db = session.get(Post, post_id)
#     if not post_db:
#         raise HTTPException(status_code=404, detail="Post not found")
#     post_data = post.model_dump(exclude_unset=True)
#     post_db.sqlmodel_update(post_data)
#     session.add(post_db)
#     session.commit()
#     session.refresh(post_db)
#     return post_db
        
    


# @app.delete("/posts/{post_id}")
# def delete_hero(post_id: int, session: Session = Depends(get_session)):
#     post = session.get(Post, post_id)
#     if not post:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(post)
#     session.commit()
#     return {"ok":True}

# @app.post("/users", response_model=UserPublic)
# def create_user(user: UserCreate,  session: Session = Depends(get_session)):
    
#     #hash the password - user.password
#     hashed_password = utilities.hash(user.password)
#     user.password = hashed_password
    
#     db_user = User.model_validate(user)
#     session.add(db_user)
#     session.commit()
#     session.refresh(db_user)
    
    
#     return db_user

# @app.get('/users/{user_nickname}')
# def get_user(user_nickname: str, session: Session = Depends(get_session)):
#     user = session.exec(select(User).where(User.nickname == user_nickname)).first()
    
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with nickname: {user_nickname} does not exist")
        
#     return user
    

