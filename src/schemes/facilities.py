from pydantic import BaseModel


class Facilities(BaseModel):
    id: int
    title: str


class FacilitiesAddRequest(BaseModel):
    title: str
