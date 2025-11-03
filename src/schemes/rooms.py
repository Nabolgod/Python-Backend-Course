from pydantic import BaseModel, Field


class RoomAddResponse(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(default=None)
    price: int
    quantity: int


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = Field(default=None)
    price: int
    quantity: int


class Room(RoomAddResponse):
    id: int


class RoomPatch(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)


class RoomPut(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
