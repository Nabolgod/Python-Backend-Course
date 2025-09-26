from fastapi import FastAPI, Query, Body, Path
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi_hotel"},
    {"id": 2, "title": "Dubai", "name": "dubai_hotel"},
    {"id": 3, "title": "New York", "name": "new_york_hotel"},
    {"id": 4, "title": "Moscow", "name": "moscow_hotel"},
]


@app.get("/hotels", summary="Вернуть информацию об отелях")
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


@app.delete("/hotels/{hotel_id}", summary="Удалить информацию об отеле")
def delete_hotel(
        hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "success"}


@app.post("/hotels", summary="Добавить отель")
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "success"}


@app.put("/hotels/{hotel_id}", summary="Полное изменение информации об отеле")
def put_hotel(
        hotel_id: int = Path(),
        title: str = Body(embed=True),
        name: str = Body(embed=True)
):
    for hotel in hotels:
        if hotel["id"] != hotel_id:
            continue
        hotel["title"] = title
        hotel["name"] = name

    return {"status": "success"}


@app.patch("/hotels/{hotel_id}", summary="Изменение определённой информации об отеле")
def patch_hotel(
        hotel_id: int = Path(),
        title: str | None = Body(embed=True, default=None),
        name: str | None = Body(embed=True, default=None)
):
    for hotel in hotels:
        if hotel["id"] != hotel_id:
            continue
        if title:
            hotel["title"] = title
        if name:
            hotel["name"] = name

    return {"status": "success"}


# Привет с макбука
def macbook_hello():
    return "Hello Git"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
