from fastapi import APIRouter, HTTPException, Response
from src.api.dependencies import UserIdDep
from src.schemes.users import UserRequestAdd, UserAdd, UserAuthentication
from src.services.auth import auth_service
from src.api.dependencies import DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", description="Регистрация пользователя")
async def register_user(
        data: UserRequestAdd,
        db: DBDep,
):
    hashed_password = auth_service.hashed_password(data.password)

    new_data = data.model_dump(exclude={"password"})  # Оставлеям из схемы UserRequestAdd все поля кроме password
    new_user_data = UserAdd(**new_data, hashed_password=hashed_password)

    await db.users.add(new_user_data)
    await db.commit()

    return {"status": "ok"}


@router.post("/login", description="Аутентификация пользователя")
async def login_user(
        data: UserAuthentication,
        response: Response,
        db: DBDep,
):
    user = await db.users.get_hash_password_or_none(email=data.email)

    if not user or not auth_service.verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Неправильно введён логин или пароль"
        )

    access_token = auth_service.create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
        user_id: UserIdDep,
        db: DBDep,
):
    users = await db.users.get_on_or_none(id=user_id)
    return {"data": users}


@router.post("/logout")
async def logout_user(
        response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "ok"}
