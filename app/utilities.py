from datetime import datetime, timedelta, timezone
from typing import Union
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from sqlmodel import Session, select
from . import models, database
from .config import settings



#SECRET_KEY
#Algorithm
#Expriation time


# === 인증 스킴 (OAuth2PasswordBearer) ===
# 공식문서: tokenUrl="token" 이지만, 우린 '/login' 사용 중
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# === 패스워드 해시 ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hasehed_password):
    return pwd_context.verify(plain_password, hasehed_password)


# === create_access_token ===
def create_access_token(data: dict, expires_delta: Union[timedelta,None] = None):
    """
    data: {"user_id": ..., ...}
    expires_delta: 만료기간 (기본 30분)
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
 
def verify_access_token(token: str, credentials_exception):
    """
    JWT 토큰 디코드 + 'user_id' 추출
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    
        user_id: str = payload.get("user_id")
    
        if user_id is None:
            raise credentials_exception
        token_data = models.TokenData(id=user_id)
    
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data
    
    
def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(database.get_session)):
    
    credentials_excpetion = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authentiate": "Bearer"})
    
    
    token_data = verify_access_token(token, credentials_excpetion)
    
    user = session.exec(select(models.User).where(models.User.id == token_data.id)).first()
    
    return user