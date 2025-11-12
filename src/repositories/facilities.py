from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM
from src.schemes.facilities import Facilities
from sqlalchemy import select


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    scheme = Facilities

    async def get_all_facilities(
            self,
            title,
    ):
        query = select(self.model)

        if title is not None:
            query = query.where(self.model.title.ilike(f'%{title.strip()}%'))

        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.scheme.model_validate(model, from_attributes=True) for model in models]
