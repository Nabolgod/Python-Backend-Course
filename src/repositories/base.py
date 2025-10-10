from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def exists(self, **filter_by):
        """
        Проверка существования записи
        """
        query = (
            select(self.model)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_all(self, *args, **kwargs):
        """Метод возвращает всю информацию по сущности"""

        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_on_or_none(self, **filter_by):
        """
        Метод возвращает None, если нет результатов или одну строчку.
        С учётом фильтров в dict filter_by.
        """
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        """
        Метод добавляет данные об сущности в базу данных
        """
        add_data_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        """
        Метод для редактирования данных с фильтрацией
        """
        put_data_stmt = (
            update(self.model)
            .values(**data.model_dump())
            .filter_by(**filter_by)
        )
        await self.session.execute(put_data_stmt)

    async def delete(self, **filter_by) -> None:
        """
        Метод для удаления данных
        """
        delete_data_stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        await self.session.execute(delete_data_stmt)
