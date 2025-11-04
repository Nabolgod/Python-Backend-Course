from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemes.bookings import BookingAddRequest, BookingAddResponse
from src.api.rooms import get_room

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        data_booking: BookingAddRequest,
):

    room = await get_room(data_booking.room_id, db)
    if room is None:
        raise HTTPException(
            status_code=404,
            detail=f"Номера с ID-{data_booking.room_id} нет",
        )
    price = room.price

    new_data_booking = BookingAddResponse(user_id=user_id, price=price, **data_booking.model_dump())

    booking = await db.bookings.add(new_data_booking)
    await db.commit()

    return {"status": "Бронирование успешно добавлено", "data": booking}
