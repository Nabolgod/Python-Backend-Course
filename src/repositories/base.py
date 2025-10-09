from sqlalchemy import select


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
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
