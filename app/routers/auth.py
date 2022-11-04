from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import or_
from app.core.auth import get_access_token
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.schemal import Capcha
from app.models.user import User
from app.utils import password
import requests
import re


router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/login')
def login(userCredentials:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):

    check_number = userCredentials.username.isnumeric()
    if check_number is True:
        if not re.match(r"^(?=.*\d)(?=.*[0-9]).{10,10}$", userCredentials.username):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'authorization': f"Sai số điện thoại.",
                    'type': 'type_error.invalid'
                }]
            )
        
    else:
        if not re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", userCredentials.username):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'authorization': f"Sai email hoặc số điện thoại.",
                    'type': 'type_error.invalid'
                }]
            )


    user_query = db.query(User).filter(or_(User.email == userCredentials.username.lower(), User.phone == userCredentials.username))
    user = user_query.first()

    if user.active is False:
        raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'authorization': f"Tài khoản của bạn đã bị khóa, vui lòng liên hệ admin@nghenongviet.vn để biết thêm chi tiết.",
                }]
            )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")

    if not password.verify(userCredentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")
            
    token = get_access_token({"user_id": user.id})
    
    return {"access_token": token, "token_type": "bearer"}


@router.post('/verify-capcha')
def verify_capcha(postData: Capcha):
    res = requests.post(f'https://www.google.com/recaptcha/api/siteverify?secret=6LcBsgQhAAAAAFFiMdkZo2UAEjW3GVRuRXvbOXan&response={postData.token}')
    if res.json()["success"] == True: 
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)