from fastapi import APIRouter, HTTPException, Response, Request
from src.repositories.users import UsersRepository
from src.schemes.users import UserRequestAdd, UserAdd, UserAuthentication
from src.database import async_session_maker
from src.services.auth import auth_service

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", description="Регистрация пользователя")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = auth_service.hashed_password(data.password)

    new_data = data.model_dump(exclude={"password"})  # Оставлеям из схемы UserRequestAdd все поля кроме password
    new_user_data = UserAdd(**new_data, hashed_password=hashed_password)

    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "ok"}


@router.post("/login", description="Аутентификация пользователя")
async def login_user(
        data: UserAuthentication,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_hash_password_or_none(email=data.email)
        if not user or not auth_service.verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Неправильно введён логин или пароль"
            )
        access_token = auth_service.create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/only_auth")
async def only_auth(
        request: Request
):
    access_token = request.cookies.get("access_token", None)
    return {"access_token": access_token}
