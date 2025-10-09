from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository
from sqlalchemy import select


class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(self, title, location, limit, offset):
        query = select(self.model)
        if title is not None:
            query = query.filter(HotelsORM.title.ilike(f'%{title}%'))
        if location is not None:
            query = query.filter(HotelsORM.location.ilike(f'%{location}%'))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return result.scalars().all()


