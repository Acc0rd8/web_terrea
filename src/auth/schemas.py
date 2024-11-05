from pydantic import BaseModel, EmailStr

#User
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserAuth(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    username: str
    email: EmailStr
    registred_at: str
    role_id: int


class UserUpdate(BaseModel):
    username: str
    email: EmailStr
    password: str
    

#Token
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str