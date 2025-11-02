from fastapi import APIRouter, Body, Query
from src.schemes.rooms import RoomAdd
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.api.hotels import get_hotel


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
    hotel = await get_hotel(room_data.hotel_id)

    if hotel is None:
        return {"status": "error", "detail": "Отеля с ID-{hotel_id} не существует"}

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
async def put_room():
    pass


@router.patch(
    "/{hotel_id}/room/{room_id}", summary="Изменить частичную информацию об отеле"
)
async def patch_room():
    pass
