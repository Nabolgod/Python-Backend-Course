from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository
from sqlalchemy import select
from src.schemes.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    scheme = Hotel

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
        models = result.scalars().all()
        return [self.scheme.model_validate(model, from_attributes=True) for model in models]
