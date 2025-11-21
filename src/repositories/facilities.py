from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.mappers.mappers import FacilitiesDataMapper, RoomsFacilitiesDataMapper
from src.schemes.facilities import RoomFacilityAdd
from sqlalchemy import select, delete


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilitiesDataMapper

    async def get_all_facilities(self, title):
        query = select(self.model)

        if title is not None:
            query = query.where(self.model.title.ilike(f'%{title.strip()}%'))

        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in models]


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    mapper = RoomsFacilitiesDataMapper

    async def get_ids_facilities(self, room_id):
        query = (
            select(self.model.facility_id)
            .where(self.model.room_id == room_id)
        )
        result = await self.session.execute(query)
        ids_facilities = result.scalars().all()
        return set(ids_facilities)

    async def delete_facilities(self, room_id: int, delete_ids: set[int]):
        if not delete_ids:
            return

        delete_data_stmt = (
            delete(self.model)
            .where(
                self.model.room_id == room_id,
                self.model.facility_id.in_(delete_ids)
            )
        )
        await self.session.execute(delete_data_stmt)

    async def update_room_facilities(
            self,
            room_id,
            facilities_ids,
    ):

        all_facility_ids = await self.get_ids_facilities(room_id)

        delete_ids = all_facility_ids - facilities_ids
        await self.delete_facilities(room_id=room_id, delete_ids=delete_ids)

        add_ids = facilities_ids - all_facility_ids
        if add_ids:
            rooms_facilities_data = [
                RoomFacilityAdd(room_id=room_id, facility_id=f_id)
                for f_id in add_ids
            ]
            await self.add_bulk(rooms_facilities_data)
