from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Request, HTTPException, status

from src.config import SECRET_KEY, ALGORITHM
from src.auth.schemas import TokenData, Token
from src.auth.crud import get_user_id, get_user
from src.database import async_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({'exp': expire})
    
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token not found'
        )
    return token


async def get_current_user(token: Annotated[str, Depends(get_token)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is invalid'
        )
        
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if not expire or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен истёк'
        )
        
    user_id = int(payload.get('sub'))
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не найден ID пользователя'
        )
    
    async with async_session() as session:
        user = await get_user(session, user_id)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found'
        )
        return user
