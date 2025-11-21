from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from sqlalchemy import select, or_
from src.repositories.mappers.mappers import HotelsDataMapper
from src.utils.repositories import rooms_ids_fro_booking


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelsDataMapper

    async def get_all_filtered_time(
            self,
            date_from,
            date_to,
            title,
            location,
            limit,
            offset,
    ):
        rooms_freedom_ids = rooms_ids_fro_booking(date_from, date_to)
        hotel_freedom_ids = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .where(RoomsORM.id.in_(rooms_freedom_ids))
        )

        query = (
            select(self.model)
            .where(self.model.id.in_(hotel_freedom_ids))
        )

        if title is not None or location is not None:
            conditions = []
            if location is not None:
                conditions.append(self.model.location.ilike(f'%{location.strip()}%'))
            if title is not None:
                conditions.append(self.model.title.ilike(f'%{title.strip()}%'))

            query = query.where(or_(*conditions))
            query = (
                query
                .limit(limit)
                .offset(offset)
            )

        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in models]
