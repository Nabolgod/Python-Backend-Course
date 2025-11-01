from fastapi import APIRouter

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.post("/{hotel_id}/room", summary="Добавить номер к отелю")
async def create_room():
    pass


@router.get("/{hotel_id}/room", summary="Вернуть информацию по номерам отеля")
async def get_rooms():
    pass


@router.get("/{hotel_id}/room/{room_id}", summary="Вернуть информацию по конкретному номеру")
async def get_room():
    pass


@router.delete("/{hotel_id}/room/{room_id}", summary="Удалить конкретный номер")
async def delete_room():
    pass


@router.put("/{hotel_id}/room/{room_id}", summary="Изменить полную информацию об отеле")
async def put_room():
    pass


@router.patch("/{hotel_id}/room/{room_id}", summary="Изменить частичную информацию об отеле")
async def patch_room():
    pass
