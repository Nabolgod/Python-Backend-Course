from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, gt=0)]
    per_page: Annotated[int | None, Query(default=3, gt=0, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]
