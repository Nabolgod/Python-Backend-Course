from fastapi import APIRouter, Body, Query, HTTPException
from src.schemes.rooms import RoomAdd, RoomPATCH, RoomPUT
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.services.rooms import room_service

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.post("/room", summary="Добавить номер к отелю")
async def create_room(
        room_data: RoomAdd = Body(
            openapi_examples={
                "1": {
                    "summary": "Пример отеля",
                    "value": {
                        "hotel_id": "(INT) Тут ID отеля",
                        "title": "Тут название номера",
                        "description": "Тут необязательная дополнительная информация",
                        "price": "(INT) Тут цена номера в сутки",
                        "quantity": "(INT) Тут кол-во персон",
                    },
                }
            }
        ),
):
    if room_service.does_room_exist(room_data.hotel_id):
        async with async_session_maker() as session:
            room = await RoomsRepository(session).add(room_data)
            await session.commit()

    return {"status": "Номер успешно добавлен", "data": room}


@router.get("/{hotel_id}/room", summary="Вернуть информацию по номерам отеля")
async def get_rooms(
        hotel_id: int,
        title: str | None = Query(default=None, description="Название номера"),
        min_price: int = Query(default=0, description="Минимальная цена номера"),
        max_price: int | None = Query(default=None, description="Максимальная цена номера"),
        min_quantity: int = Query(default=1, description="Минимальное кол-во персон"),
        max_quantity: int | None = Query(
            default=None, description="Максимальное кол-во персон"
        ),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id,
            title,
            min_price,
            max_price,
            min_quantity,
            max_quantity,
        )


@router.get(
    "/{hotel_id}/room/{room_id}", summary="Вернуть информацию по конкретному номеру"
)
async def get_room(
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_on_or_none(
            hotel_id=hotel_id, id=room_id
        )


@router.delete("/{hotel_id}/room/{room_id}", summary="Удалить конкретный номер")
async def delete_room(
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"starus": "ok", "detail": f"Номер с ID-{room_id} удалён"}


@router.put("/{hotel_id}/room/{room_id}", summary="Изменить полную информацию об отеле")
async def put_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPUT,
):
    if await get_room(hotel_id, room_id) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Отеля с ID-{hotel_id} или номера с ID-{room_id} не существует"
        )
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"starus": "ok", "detail": f"Номер с ID-{room_id} полностью изменён"}


@router.patch(
    "/{hotel_id}/room/{room_id}", summary="Изменить частичную информацию об отеле"
)
async def patch_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPATCH,
):
    if await get_room(hotel_id, room_id) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Отеля с ID-{hotel_id} или номера с ID-{room_id} не существует"
        )
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"starus": "ok", "detail": f"Номер с ID-{room_id} частично изменён"}
