from pydantic import BaseModel, EmailStr, Field


# Схема для приёма данных от пользователя через api
class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    nick_name: str
    number: str | None = Field(default=None)


# Схема для отправки в базу данных
class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    nick_name: str
    number: str | None = Field(default=None)


# Схема для получения данных
class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    nick_name: str
    number: str | None = Field(default=None)
