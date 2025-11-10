from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel


class BaseRepository:
    model = None
    scheme: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        """Метод возвращает всю информацию по сущности"""

        query = select(self.model)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.scheme.model_validate(model, from_attributes=True) for model in models]

    async def get_all_filtered(self, *where, **filter_by):
        """Метод возвращает всю информацию по сущности с учётом фильтрации"""

        query = (
            select(self.model)
            .filter(*where)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.scheme.model_validate(model, from_attributes=True) for model in models]

    async def get_on_or_none(self, **filter_by):
        """
        Метод возвращает None, если нет результатов или одну строчку.
        С учётом фильтров в dict filter_by.
        """
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.scheme.model_validate(model, from_attributes=True)

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
        model = result.scalars().one()
        return self.scheme.model_validate(model, from_attributes=True)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        """
        Метод для редактирования данных с фильтрацией
        """
        put_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
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
