import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Post(SQLModel, table = True):
    id : int = Field(primary_key=True)
    title : str 
    content : str
    published : bool = Field(default=True)
    created_at : datetime = Field(default_factory=datetime)
    
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables(): #To create Table
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.post("/posts/")
def create_post(post: Post, session: Session) -> Post:
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@app.get("/posts")
def read_posts(
    session: Session,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Post]:
    posts = session.exec(select(Post).offset(posts).limit(limit).all())
    return posts

@app.get("/posts/{post_id}")
def read_post(post_id: int, session: Session) -> Post:
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Hero not found")
    return post

@app.delete("/posts/{post_id}")
def delete_hero(post_id: int, session: Session):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(post)
    session.commit()
    return {"ok":True}



    

