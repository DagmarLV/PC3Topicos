import os
from functools import wraps
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from ..database import SessionLocal
from .. import models, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = schemas.TokenData(email=email)
        except JWTError:
            raise credentials_exception

        user = db.query(models.User).filter(models.User.email == token_data.email).first()
        if user is None:
            raise credentials_exception
        return user
    finally:
        db.close()

def authenticated(func):
    @wraps(func)
    async def wrapper(*args, request=None, current_user: models.User = Depends(authenticate_user), **kwargs):
        return await func(*args, request=request, current_user=current_user, **kwargs)
    return wrapper
