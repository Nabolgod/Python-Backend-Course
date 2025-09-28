from fastapi import Query, APIRouter, Body
import time
import asyncio
import threading
from schemes.hotels import Hotel, HotelPATCH
from dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("/sync/{id}", summary="Синхронная ручкаа по возврату отеля")
def sync_get(hotel_id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    print(f"sync. Нaчал {hotel_id}: {round(time.time(), 2)}")
    time.sleep(3)
    print(f"sync. Закончил {hotel_id}: {round(time.time(), 2)}")
    hotel = [h for h in hotels if h["id"] == hotel_id]
    return hotel


@router.get("/async/{id}", summary="Асинхронная ручка по возврату отеля")
async def async_get(hotel_id: int):
    print(f"async. Потоков: {threading.active_count()}")
    print(f"async. Нaчал {hotel_id}: {round(time.time(), 2)}")
    await asyncio.sleep(3)
    print(f"async. Закончил {hotel_id}: {round(time.time(), 2)}")
    hotel = [h for h in hotels if h["id"] == hotel_id]
    return hotel


@router.get("", summary="Вернуть информацию об отелях")
def get_hotels(
        pagination: PaginationDep,
        hotel_id: int | None = Query(default=None, description="ID-номер"),
        title: str | None = Query(default=None, description="Название отеля"),
):
    return_hotels = []
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        return_hotels.append(hotel)

    current_page = pagination.page
    limit_page = (len(return_hotels) // pagination.per_page) + (
        1 if len(return_hotels) % pagination.per_page != 0 else 0)
    if pagination.page > limit_page:
        current_page = limit_page
    return return_hotels[(current_page - 1) * pagination.per_page: current_page * pagination.per_page]


@router.delete("/{hotel_id}", summary="Удалить информацию об отеле")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "success"}


@router.post("", summary="Добавить отель")
def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            "1": {"summary": "Сочи", "value": {
                "title": "Отель Сочии 5 звёзд у моря",
                "name": "sochi_hotel",
            }}
        }),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "success"}


@router.put("/{hotel_id}", summary="Полное изменение информации об отеле")
def put_hotel(
        hotel_id: int,
        hotel_data: Hotel,
):
    for hotel in hotels:
        if hotel["id"] != hotel_id:
            continue
        hotel["title"] = hotel_data.title
        hotel["name"] = hotel_data.name

    return {"status": "success"}


@router.patch("/{hotel_id}", summary="Изменение определённой информации об отеле")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    for hotel in hotels:
        if hotel["id"] != hotel_id:
            continue
        if hotel_data.title:
            hotel["title"] = hotel_data.title
        if hotel_data.name:
            hotel["name"] = hotel_data.name

    return {"status": "success"}
