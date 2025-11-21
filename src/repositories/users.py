from pydantic import EmailStr
from sqlalchemy import select
from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UsersDataMapper
from src.schemes.users import UserWithHashPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UsersDataMapper

    async def get_hash_password_or_none(self, email: EmailStr):
        """
        Метод возвращает None, если нет результатов или одну строчку.
        С учётом фильтров в dict filter_by.
        """
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashPassword.model_validate(model, from_attributes=True)
