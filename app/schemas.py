from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import date

class PostContact(BaseModel):
    name:str = Field(title="Name of a person in question", min_length=1, max_length=20)
    surname:str | None = Field(title="Surname of a person in question", min_length=1, max_length=35, default=None)
    mail:str | None = Field(title="Email of a person in question", min_length=1, max_length=50, pattern="\S{3,}@[a-zA-Z]{2,}\.[a-zA-Z]{2,}", default=None)
    phone:str = Field(title="Phone of a person in question", min_length=10, max_length=12, pattern="\d{10}", default=None)
    birthday:date | None = Field(title="B-day of a person in question", default=None)

    class Config:
        from_attributes = True

class ResponseContact(PostContact):
    id:int

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr
    
class EmailSchema(BaseModel):
    email: EmailStr
