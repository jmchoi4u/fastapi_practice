# app/database.py
from sqlmodel import create_engine, Session
from .config import settings


DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(DATABASE_URL)

def get_session():
    """
    FastAPI에서 종속성(Dependency)으로 사용할 함수.
    요청이 들어오면 세션 열고, 요청 끝나면 세션 닫음.
    """
    with Session(engine) as session:
        yield session