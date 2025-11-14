from pydantic import BaseModel


class Facility(BaseModel):
    id: int
    title: str


class FacilityAdd(BaseModel):
    title: str


class RoomFacility(BaseModel):
    id: int
    room_id: int
    facility_id: int


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int
