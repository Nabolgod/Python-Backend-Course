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
    facilities_ids: list[int] | None = Field(default=None)


class Room(RoomAddResponse):
    id: int


class RoomPatchResponse(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)
    facilities_ids: set[int] | None = Field(default=None)


class RoomPatchRequest(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)


class RoomPutResponse(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
    facilities_ids: set[int]


class RoomPutRequest(BaseModel):
    title: str
    description: str
    price: int
    quantity: int
