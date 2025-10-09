from sqlalchemy import select, insert


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

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

    async def add(self, scheme_data):
        """
        Метод добавляет данные об сущности в базу данных
        """
        add_stmt = (
            insert(self.model)
            .values(**scheme_data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(add_stmt)
        return result.scalar_one()
