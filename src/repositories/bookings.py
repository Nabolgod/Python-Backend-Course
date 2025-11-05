from src.repositories.base import BaseRepository
from src.models.bookings import BookingORM
from src.schemes.bookings import Booking
from sqlalchemy import select


class BookingRepository(BaseRepository):
    model = BookingORM
    scheme = Booking

    async def get_all_my_bookings(self, user_id):
        query = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.scheme.model_validate(model, from_attributes=True) for model in models]
