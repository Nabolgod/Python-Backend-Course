from datetime import date, timedelta
from fastapi import APIRouter, Body, Query, HTTPException
from src.schemes.rooms import (
    RoomAddRequest, RoomAddResponse,
    RoomPatchResponse, RoomPatchRequest,
    RoomPutResponse, RoomPutRequest
)
from src.schemes.facilities import RoomFacilityAdd
from src.services.rooms import room_service
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.post("/{hotel_id}/room", summary="Добавить номер к отелю")
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(),
):
    room = None
    if await room_service.does_hotel_exist(hotel_id, db):
        new_room_data = RoomAddResponse(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
        room = await db.rooms.add(new_room_data)

    if room_data.facilities_ids is not None:
        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id)
            for f_id in room_data.facilities_ids
        ]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "Номер успешно добавлен", "data": room}


@router.get("/{hotel_id}/rooms", summary="Вернуть информацию по номерам отеля")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        title: str | None = Query(default=None, description="Название номера"),
        min_price: int = Query(default=0, description="Минимальная цена номера"),
        max_price: int | None = Query(default=None, description="Максимальная цена номера"),
        min_quantity: int = Query(default=1, description="Минимальное кол-во номеров"),
        max_quantity: int | None = Query(
            default=None, description="Максимальное кол-во номеров"
        ),
):
    return await db.rooms.get_all(
        hotel_id,
        title,
        min_price,
        max_price,
        min_quantity,
        max_quantity,
    )


@router.get("/{hotel_id}/rooms/free", summary="Вернуть информацию по свободным отелям в определённые даты")
async def get_rooms_freedom(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example=f"{date.today()}"),
        date_to: date = Query(example=f"{date.today() + timedelta(days=10)}"),
):
    return await db.rooms.get_all_filtered_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )


@router.get(
    "/room/{room_id}", summary="Вернуть информацию по конкретному номеру"
)
async def get_room(
        room_id: int,
        db: DBDep,
):
    return await db.rooms.get_on_or_none(id=room_id)


@router.delete("/{hotel_id}/room/{room_id}", summary="Удалить конкретный номер")
async def delete_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()

    return {"starus": "ok", "detail": f"Номер с ID-{room_id} удалён"}


@router.put("/{hotel_id}/room/{room_id}", summary="Изменить полную информацию о номере")
async def put_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPutResponse,
        db: DBDep,
):
    if await get_room(room_id, db) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Номера с ID-{room_id} не существует"
        )

    new_room_data = RoomPutRequest(**room_data.model_dump(exclude={"facilities_ids"}))
    await db.rooms.edit(data=new_room_data, hotel_id=hotel_id, id=room_id)
    await db.rooms_facilities.update_room_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"starus": "ok", "detail": f"Номер с ID-{room_id} полностью изменён"}


@router.patch(
    "/{hotel_id}/room/{room_id}", summary="Изменить частичную информацию о номере"
)
async def patch_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchResponse,
        db: DBDep,
):
    if await get_room(room_id, db) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Номера с ID-{room_id} не существует"
        )

    new_room_data = RoomPatchRequest(**room_data.model_dump(exclude={"facilities_ids"}))
    await db.rooms.edit(data=new_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await db.rooms_facilities.update_room_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()

    return {"starus": "ok", "detail": f"Номер с ID-{room_id} частично изменён"}
