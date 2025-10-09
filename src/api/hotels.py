from fastapi import Query, APIRouter, Body
import time
import asyncio
import threading
import sqlalchemy as alh

from src.repositories.hotels import HotelsRepository
from src.schemes.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsORM

router = APIRouter(prefix="/hotels", tags=["Отели"])


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


@router.get("", summary="Вернуть информацию об отелях")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Расположение отеля"),

):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).get_all()
    return result


# @router.delete("/{hotel_id}", summary="Удалить информацию об отеле")
# def delete_hotel(hotel_id: int):
#     global hotels
#     hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
#     return {"status": "success"}


@router.post("", summary="Добавить отель")
async def create_hotel(
        hotel_data: Hotel = Body(
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
        add_hotel_stmt = alh.insert(HotelsORM).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "Отель успешно добавлен!"}

# @router.put("/{hotel_id}", summary="Полное изменение информации об отеле")
# def put_hotel(
#         hotel_id: int,
#         hotel_data: Hotel,
# ):
#     for hotel in hotels:
#         if hotel["id"] != hotel_id:
#             continue
#         hotel["title"] = hotel_data.title
#         hotel["name"] = hotel_data.name
#
#     return {"status": "success"}


# @router.patch("/{hotel_id}", summary="Изменение определённой информации об отеле")
# def patch_hotel(
#         hotel_id: int,
#         hotel_data: HotelPATCH,
# ):
#     for hotel in hotels:
#         if hotel["id"] != hotel_id:
#             continue
#         if hotel_data.title:
#             hotel["title"] = hotel_data.title
#         if hotel_data.name:
#             hotel["name"] = hotel_data.name
#
#     return {"status": "success"}
