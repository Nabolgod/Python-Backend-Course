from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemes.rooms import Room
from sqlalchemy import select
from src.utils.repositories import rooms_ids_fro_booking


class RoomsRepository(BaseRepository):
    model = RoomsORM
    scheme = Room

    async def get_all(
            self,
            hotel_id,
            title,
            min_price,
            max_price,
            min_quantity,
            max_quantity,
    ):
        query = select(self.model).filter_by(hotel_id=hotel_id)

        if title is not None:
            query = query.filter(self.model.title.ilike(f'%{title}%'))

        if max_price is not None:
            query = query.where(self.model.price.between(min_price, max_price))

        if max_quantity is not None:
            query = query.where(self.model.quantity.between(min_quantity, max_quantity))

        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.scheme.model_validate(model, from_attributes=True) for model in models]

    async def get_all_filtered_time(
            self,
            hotel_id,
            date_from,
            date_to,
    ):
        rooms_freedom_ids = rooms_ids_fro_booking(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )
        return await self.get_all_filtered(self.model.id.in_(rooms_freedom_ids))
