'''
Create
Read
Update
Delete
'''


from typing import Annotated
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from fastapi import Depends

from src.auth.models import User
from src.auth.schemas import UserCreate, UserUpdate
from src.database import get_async_session

session_db = Annotated[async_sessionmaker, Depends(get_async_session)]


#Create
async def create_user(session: session_db, user_in: UserCreate) -> dict:
    stmt = insert(User).values(**user_in.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {'message': 'success'}


#Read
# async def get_users(session: session_db) -> list[User]:
#     stmt = select(User).order_by(User.id)
#     result = await session.execute(stmt)
#     users = result.scalars().all()
#     return list(users)

async def get_user_id(session: session_db, user_email: str) -> int | None:
    stmt = select(User.id).where(user_email==User.email)
    result = await session.execute(stmt)
    user_id = result.scalars().all()
    if user_id is not None:
        return int(user_id[0])
    return None

async def get_user_password(session: AsyncSession, user_id: int) -> str:
    stmt = select(User.password).where(User.id==user_id)
    result = await session.execute(stmt)
    user_password = result.scalars().all()
    return str(user_password[0])

async def get_user_email(session: AsyncSession, user_id: int) -> str:
    stmt = select(User.email).where(User.id==user_id)
    result = await session.execute(stmt)
    user_email = result.scalars().all()
    return str(user_email[0])

async def get_user(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(user_id==User.id)
    result = await session.execute(stmt)
    user = result.scalars().all()
    return user


#Update
async def update_user(session: session_db, user_old_id: int, user_new: UserUpdate) -> User: #TODO
    new_user_dict = user_new.model_dump(exclude_unset=True)
    stmt = update(User).where(User.id == user_old_id).values(new_user_dict).returning(User) #TODO
    result = await session.execute(stmt)
    await session.commit()
    return result.first()

#Delete
async def delete_user(session: session_db, user_id: int) -> dict:
    pass #TODO