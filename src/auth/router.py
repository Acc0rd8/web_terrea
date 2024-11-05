from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Annotated

from src.auth.schemas import UserCreate, UserAuth
from src.database import async_session
from src.auth.crud import get_user, create_user, get_user_id, get_user_email, get_user_password
from src.auth.basic_config import get_password_hash, verify_password, create_access_token, get_current_user
from src.auth.models import User

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register/')
async def register_user(user_data: UserCreate) -> dict:
    async with async_session() as session:
        user_id = await get_user_id(session, user_data.email)
        user = await get_user(session, user_id)
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Пользователь уже существует'
            )
        user_dict = user_data.model_dump()
        user_dict['password'] = get_password_hash(user_data.password)
        await create_user(session, UserCreate(**user_dict))
        return {'message': 'Вы успешно зарегистрировались!'}
    
    
@router.post('/login/')
async def authenticate_user(response: Response, user_data: UserAuth):
    async with async_session() as session:
        user_id = await get_user_id(session, user_data.email)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неверная почта или пароль'
            )
        user_email = await get_user_email(session, user_id)
        user_password = await get_user_password(session, user_id)
        
        if user_data.email != user_email  and not verify_password(user_data.password, user_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неверная почта или пароль'
            )
        access_token = create_access_token({'sub': str(user_id)})
        response.set_cookie(key='users_access_token', value=access_token, httponly=True)
        return {'access_token': access_token, 'refresh_token': None}
    

@router.get('/me/')
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.post('/logout/')
async def logout_user(response: Response):
    response.delete_cookie(key='users_access_token')
    return {'message': 'Пользователь успешно вышел из системы'}