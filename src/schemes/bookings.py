from pydantic import BaseModel, computed_field
from datetime import date


class Booking(BaseModel):
    id: int
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingAddResponse(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int

