from fastapi import APIRouter, Body, Query, HTTPException
from src.schemes.rooms import RoomAddRequest, RoomPatch, RoomPut, RoomAddResponse
from src.services.rooms import room_service
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.post("/{hotel_id}/room", summary="Добавить номер к отелю")
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(
            openapi_examples={
                "1": {
                    "summary": "Пример отеля",
                    "value": {
                        "title": "Тут название номера",
                        "description": "Тут необязательная дополнительная информация",
                        "price": "(INT) Тут цена номера в сутки",
                        "quantity": "(INT) Тут кол-во номеров",
                    },
                }
            }
        ),
):
    room = None
    if await room_service.does_hotel_exist(hotel_id):
        new_room_data = RoomAddResponse(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
        room = await db.rooms.add(new_room_data)
        await db.commit()

    return {"status": "Номер успешно добавлен", "data": room}


@router.get("/{hotel_id}/room", summary="Вернуть информацию по номерам отеля")
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


@router.put("/{hotel_id}/room/{room_id}", summary="Изменить полную информацию об отеле")
async def put_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPut,
        db: DBDep,
):
    if await get_room(room_id, db) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Номера с ID-{room_id} не существует"
        )

    await db.rooms.edit(data=room_data, hotel_id=hotel_id, id=room_id)
    await db.commit()

    return {"starus": "ok", "detail": f"Номер с ID-{room_id} полностью изменён"}


@router.patch(
    "/{hotel_id}/room/{room_id}", summary="Изменить частичную информацию об отеле"
)
async def patch_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatch,
        db: DBDep,
):
    if await get_room(room_id, db) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Номера с ID-{room_id} не существует"
        )

    await db.rooms.edit(data=room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await db.commit()

    return {"starus": "ok", "detail": f"Номер с ID-{room_id} частично изменён"}
