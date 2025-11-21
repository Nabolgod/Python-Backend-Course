from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.repositories.mappers.mappers import BookingsDataMapper
from sqlalchemy import select


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingsDataMapper

    async def get_all_my_bookings(self, user_id):
        query = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in models]
