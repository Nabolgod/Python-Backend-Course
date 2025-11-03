from fastapi import Query, APIRouter, Body
from src.schemes.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Вернуть информацию об отелях")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Расположение отеля"),

):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pagination.page - 1))


@router.get("/{hotel_id}", summary="Вернуть отель по ID")
async def get_hotel(
        hotel_id: int,
        db: DBDep,
):
    return await db.hotels.get_on_or_none(id=hotel_id)


@router.delete("/{hotel_id}", summary="Удалить информацию об отеле")
async def delete_hotel(
        hotel_id: int,
        db: DBDep,
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "success", "message": f"Отель {hotel_id} удален"}


@router.post("", summary="Добавить отель")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "title": "Отдых наяву, а не во сне",
                        "location": "Лучший город Сочи",
                    },
                }
            }
        ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "Отель успешно добавлен!",
            "data": hotel}


@router.put("/{hotel_id}", summary="Полное изменение информации об отеле")
async def put_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
        db: DBDep,
):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "success", "message": f"Отель {hotel_id} обновлен"}


@router.patch("/{hotel_id}", summary="Изменение определённой информации об отеле")
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPatch,
        db: DBDep,
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "success", "message": f"Отель {hotel_id} частично обновлен"}
