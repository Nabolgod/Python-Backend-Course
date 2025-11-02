from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated
from src.services.auth import auth_service


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="Кол-во страниц", ge=1)]
    per_page: Annotated[int | None, Query(default=None, description="Кол-во элементов на странице", ge=1, lt=30)]

# Зависимость для пагинации
PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Не предоставлен токен")
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = auth_service.decode_token(token)
    return data.get("user_id", None)

# Зависимость на возврат id текущего пользователя
UserIdDep = Annotated[int, Depends(get_current_user_id)]

