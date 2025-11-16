from pydantic import BaseModel, Field
from typing import Optional

from src.schemes.facilities import Facility


class RoomCoreFields(BaseModel):
    title: str
    description: Optional[str] = Field(default=None)
    price: int
    quantity: int


class RoomOptionalFields(BaseModel):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[int] = Field(default=None)
    quantity: Optional[int] = Field(default=None)


# Запросы
class RoomAddRequest(RoomCoreFields):
    facilities_ids: Optional[list[int]] = Field(default=[])


class RoomPutRequest(RoomCoreFields):
    pass


class RoomPatchRequest(RoomOptionalFields):
    pass


# Ответы
class RoomAddResponse(RoomCoreFields):
    hotel_id: int


class Room(RoomCoreFields):
    id: int
    hotel_id: int


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPutResponse(RoomCoreFields):
    facilities_ids: set[int]


class RoomPatchResponse(RoomOptionalFields):
    facilities_ids: Optional[set[int]] = Field(default=set())
