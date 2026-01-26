from fastapi import APIRouter, Query, Body
from src.api.dependencies import DBDep
from src.schemes.facilities import FacilityAdd
from fastapi_cache.decorator import cache
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.post("", summary="Создать удобство")
async def create_facility(
        db: DBDep,
        facility_data: FacilityAdd = Body(),
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay()

    return {"status": "ok", "data": facility}


@router.get("", summary="Вернуть все удобства")
@cache(expire=60)
async def get_facilities(
        db: DBDep,
        title: str | None = Query(default=None, description="Название удобства"),
):
    return await db.facilities.get_all_facilities(title=title)


@router.get("/{facility_id}", summary="Вернуть удобство по ID")
@cache(expire=60)
async def get_facility(
        db: DBDep,
        facility_id: int,
):
    return await db.facilities.get_on_or_none(id=facility_id)
