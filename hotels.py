from fastapi import Query, Body, Path, APIRouter
import time
import asyncio
import threading

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi_hotel"},
    {"id": 2, "title": "Dubai", "name": "dubai_hotel"},
    {"id": 3, "title": "New York", "name": "new_york_hotel"},
    {"id": 4, "title": "Moscow", "name": "moscow_hotel"},
]


@router.get("/sync/{id}", summary="Синхронная ручкаа по возврату отеля")
def sync_get(id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    print(f"sync. Нaчал {id}: {round(time.time(), 2)}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {round(time.time(), 2)}")
    # hotel = [h for h in hotels if h["id"] == id]
    # return hotel


@router.get("/async/{id}", summary="Асинхронная ручка по возврату отеля")
async def async_get(id: int):
    print(f"async. Потоков: {threading.active_count()}")
    print(f"async. Нaчал {id}: {round(time.time(), 2)}")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {round(time.time(), 2)}")
    #
    # hotel = [h for h in hotels if h["id"] == id]
    # return hotel


@router.get("", summary="Вернуть информацию об отелях")
def get_hotels(
        id: int | None = Query(default=None, description="ID-номер"),
        title: str | None = Query(default=None, description="Название отеля"),
):
    return_hotels = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        return_hotels.append(hotel)

    return return_hotels


@router.delete("/{hotel_id}", summary="Удалить информацию об отеле")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "success"}


@router.post("", summary="Добавить отель")
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": title})
    return {"status": "success"}


@router.put("/{hotel_id}", summary="Полное изменение информации об отеле")
def put_hotel(
        hotel_id: int = Path(), title: str = Body(embed=True), name: str = Body(embed=True)
):
    for hotel in hotels:
        if hotel["id"] != hotel_id:
            continue
        hotel["title"] = title
        hotel["name"] = name

    return {"status": "success"}


@router.patch("/{hotel_id}", summary="Изменение определённой информации об отеле")
def patch_hotel(
        hotel_id: int = Path(),
        title: str | None = Body(embed=True, default=None),
        name: str | None = Body(embed=True, default=None),
):
    for hotel in hotels:
        if hotel["id"] != hotel_id:
            continue
        if title:
            hotel["title"] = title
        if name:
            hotel["name"] = name

    return {"status": "success"}
