from src.api.hotels import get_hotel
from fastapi import HTTPException


class RoomsService:
    @staticmethod
    async def does_hotel_exist(hotel_id, db):
        hotel = await get_hotel(hotel_id, db)

        if hotel is None:
            raise HTTPException(
                status_code=404,
                detail=f"Отеля с ID-{hotel_id} не существует"
            )

        return True


room_service = RoomsService()
