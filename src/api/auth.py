from fastapi import APIRouter, HTTPException, Response
from src.repositories.users import UsersRepository
from src.schemes.users import UserRequestAdd, UserAdd, UserAuthentication
from src.database import async_session_maker
from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
import jwt

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", description="Регистрация пользователя")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)

    new_data = data.model_dump(exclude={"password"})  # Оставлеям из схемы UserRequestAdd все поля кроме password
    new_user_data = UserAdd(**new_data, hashed_password=hashed_password)

    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "ok"}


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    """Создание токена при аутентификации"""
    to_encode = data.copy()
    expire = (
            datetime.now(timezone.utc) +
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля при аутентификации"""
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/login", description="Аутентификация пользователя")
async def login_user(
        data: UserAuthentication,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_hash_password_or_none(email=data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Неправильно введён логин или пароль"
            )
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
