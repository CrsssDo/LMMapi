from app.models.user import User
from fastapi import Depends, HTTPException, status
from app.utils.password import verify
from datetime import datetime, timedelta
from app.core.settings import settings, oauth2_scheme
from jose import JWTError, jwt
from app.schemas.token import TokenData
from sqlalchemy.orm import Session
from app.core.database import get_db
    
def get_access_token(data:dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_reset_password_token(data:dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=5)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_authenticated_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    user_query = db.query(User).filter(User.id == token_data.id)
    user = user_query.first()

    if user.active is False:
        raise credentials_exception

    now = datetime.now()
    if (now - user.last_logged_in_date).days >= 7:
        user_query.update({"last_logged_in_date": datetime.now()}, synchronize_session=False)
        db.commit()
        raise credentials_exception

    user_query.update({"last_logged_in_date": datetime.now()}, synchronize_session=False)     
    db.commit()

    return user