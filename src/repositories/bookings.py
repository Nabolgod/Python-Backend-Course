from src.repositories.base import BaseRepository
from src.models.bookings import BookingORM
from src.schemes.bookings import Booking


class BookingRepository(BaseRepository):
    model = BookingORM
    scheme = Booking
