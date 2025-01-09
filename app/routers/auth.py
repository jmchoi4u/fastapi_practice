from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .. import database, models, utilities

router = APIRouter(tags=['Authentication'])

@router.post("/login") # tokenUrl='login'
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), session : Session = Depends(database.get_session)):
    # user_credentials.username => 로그인 아이디(우리 경우 email)
    # user_credentials.password => 사용자가 입력한 비번
    
    user = session.query(models.User).filter(models.User.email == user_credentials.username).first()
     
    if not user: # 유저가 없음 => 403 or 401
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # 패스워드 검증
    if not utilities.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    #create a token
    #return token
    
    access_token = utilities.create_access_token(data = {"user_id": str(user.id)}) # payload에 user id
    
    return {"access_token": access_token, "token_type": "bearer"}

