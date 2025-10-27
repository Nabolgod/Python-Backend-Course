from pydantic import BaseModel, EmailStr, Field


# Схема для аутентификации
class UserAuthentication(BaseModel):
    email: EmailStr
    password: str


# Схема для регистрации user
class UserRequestAdd(UserAuthentication):
    first_name: str
    last_name: str
    nick_name: str
    number: str | None = Field(default=None)


# Схема для работы с базой данных
class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    nick_name: str
    number: str | None = Field(default=None)


# Схема для получения данных от базы
class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    nick_name: str
    number: str | None = Field(default=None)


# Схема для проверки пароля с хэшом
class UserWithHashPassword(BaseModel):
    id: int
    hashed_password: str
