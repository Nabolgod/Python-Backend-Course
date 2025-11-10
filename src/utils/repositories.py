from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from sqlalchemy import select, func
from datetime import date


def rooms_ids_fro_booking(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
):
    rooms_count = (
        select(
            BookingsORM.room_id,
            func.count("*").label("rooms_booked")
        )
        .select_from(BookingsORM)
        .where(
            BookingsORM.date_from <= date_to,
            BookingsORM.date_to >= date_from,
        )
        .group_by(BookingsORM.room_id)
        .cte(name="rooms_count")
    )
    rooms_left_table = (
        select(
            RoomsORM.id.label("room_id"),
            (RoomsORM.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("free_quantity")
        )
        .select_from(RoomsORM)
        .outerjoin(
            rooms_count,
            RoomsORM.id == rooms_count.c.room_id,
        )
    )

    if hotel_id is not None:
        rooms_left_table = (
            rooms_left_table
            .where(RoomsORM.hotel_id == hotel_id)
        )

    rooms_left_table = (
        rooms_left_table
        .cte(name="rooms_left_table")
    )

    rooms_freedom_ids = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .where(rooms_left_table.c.free_quantity > 0)
    )

    return rooms_freedom_ids
