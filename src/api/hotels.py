from fastapi import Query, APIRouter, Body, HTTPException, status
from src.repositories.hotels import HotelsRepository
from src.schemes.hotels import Hotel, HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Вернуть информацию об отелях")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Расположение отеля"),

):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await (
            HotelsRepository(session)
            .get_all(
                title=title,
                location=location,
                limit=per_page,
                offset=per_page * (pagination.page - 1))
        )


@router.get("/{hotel_id}", summary="Вернуть отель по ID")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        repository = HotelsRepository(session)

        if not await repository.exists(id=hotel_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Отеля с ID {hotel_id} не найдено"
            )
        return await repository.get_on_or_none(id=hotel_id)


@router.delete("/{hotel_id}", summary="Удалить информацию об отеле")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        repository = HotelsRepository(session)

        if not await repository.exists(id=hotel_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Отель с ID {hotel_id} не найден"
            )

        await repository.delete(id=hotel_id)
        await session.commit()

    return {"status": "success", "message": f"Отель {hotel_id} удален"}


@router.post("", summary="Добавить отель")
async def create_hotel(
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
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "Отель успешно добавлен!",
            "data": hotel}


@router.put("/{hotel_id}", summary="Полное изменение информации об отеле")
async def put_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
):
    async with async_session_maker() as session:
        repository = HotelsRepository(session)

        if not await repository.exists(id=hotel_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Отель с ID {hotel_id} не найден"
            )
        await repository.edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "success", "message": f"Отель {hotel_id} обновлен"}


@router.patch("/{hotel_id}", summary="Изменение определённой информации об отеле")
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        repository = HotelsRepository(session)

        if not await repository.exists(id=hotel_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Отель с ID {hotel_id} не найден"
            )
        await repository.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {"status": "success", "message": f"Отель {hotel_id} частично обновлен"}

# @router.get("/sync/{id}", summary="Синхронная ручкаа по возврату отеля")
# def sync_get(hotel_id: int):
#     print(f"sync. Потоков: {threading.active_count()}")
#     print(f"sync. Нaчал {hotel_id}: {round(time.time(), 2)}")
#     time.sleep(3)
#     print(f"sync. Закончил {hotel_id}: {round(time.time(), 2)}")
#     hotel = [h for h in hotels if h["id"] == hotel_id]
#     return hotel


# @router.get("/async/{id}", summary="Асинхронная ручка по возврату отеля")
# async def async_get(hotel_id: int):
#     print(f"async. Потоков: {threading.active_count()}")
#     print(f"async. Нaчал {hotel_id}: {round(time.time(), 2)}")
#     await asyncio.sleep(3)
#     print(f"async. Закончил {hotel_id}: {round(time.time(), 2)}")
#     hotel = [h for h in hotels if h["id"] == hotel_id]
#     return hotel
