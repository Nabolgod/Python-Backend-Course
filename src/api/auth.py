from fastapi import APIRouter

from src.repositories.users import UsersRepository
from src.schemes.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from passlib.context import CryptContext

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
