from fastapi import APIRouter, Query
from src.api.dependencies import DBDep
from src.schemes.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.post("/", summary="Создать удобство")
async def create_facility(
        db: DBDep,
        facility_data: FacilityAdd,
):
    await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "ok", "data": facility_data}


@router.get("/", summary="Вернуть все удобства")
async def get_facilities(
        db: DBDep,
        title: str | None = Query(default=None, description="Название удобства"),
):
    return await db.facilities.get_all_facilities(title=title)


@router.get("/{facility_id}", summary="Вернуть удобство по ID")
async def get_facility(
        db: DBDep,
        facility_id: int,
):
    return await db.facilities.get_on_or_none(id=facility_id)
