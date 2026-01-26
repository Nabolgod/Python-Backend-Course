from fastapi import APIRouter, HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemes.bookings import BookingAddRequest, BookingAddResponse
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Создать бронирование")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        data_booking: BookingAddRequest,
):
    room = await db.rooms.get_on_or_none(id=data_booking.room_id)
    if room is None:
        raise HTTPException(
            status_code=404,
            detail=f"Номера с ID-{data_booking.room_id} нет",
        )
    price = room.price

    new_data_booking = BookingAddResponse(
        user_id=user_id,
        price=price,
        **data_booking.model_dump(),
    )

    booking = await db.bookings.add(new_data_booking)
    await db.commit()

    return {"status": "Бронирование успешно добавлено", "data": booking}


@router.get("/bookings", summary="Вернуть все бронирования")
@cache(expire=60)
async def get_bookings(
        db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/bookings/me", summary="Вернуть все бронирования авторизованного пользователя")
@cache(expire=60)
async def get_bookings_me(
        db: DBDep,
        user_id: UserIdDep,
):
    return await db.bookings.get_all_my_bookings(user_id=user_id)
