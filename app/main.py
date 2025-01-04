import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, SQLModel, Session, create_engine, select


class Posts(SQLModel, table =True):
    id : int = Field(default=None, primary_key = True)
    title : str
    content : str
    published : bool = Field(default=True)
    created_at : datetime = Field(default_factory=datetime)
    
postgresql_url = ""