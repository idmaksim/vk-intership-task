TEMPLATE = """
from sqlalchemy.exc import IntegrityError

from abstract_repo import SQLAlchemyRepository, AbstractRepository
from db import {kind}
from fastapi import HTTPException
from schemas import YourModelUpdateSchema, YourModelCreateSchema


class {kind}Repository(SQLAlchemyRepository):
    model = {kind}


class {kind}Service:
    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def create(self, item: YourModelCreateSchema):
        item_dict = item.model_dump()
        try:
            return await self.repository.create(item_dict)
        except IntegrityError:
            raise HTTPException(
                detail="conflict error",
                status_code=409
            )

    async def get_all(self, limit: int, offset: int):
        if items := await self.repository.read_all(limit, offset):
            return items
        raise HTTPException(
                detail="not found",
                status_code=404
            )

    async def get_by_id(self, id: int):
        if item := await self.repository.read_by_id(id):
            return item
        raise HTTPException(
                detail="not found",
                status_code=404
            )

    async def update(self, id: int, item: YourModelUpdateSchema):
        item_dict = item.model_dump()
    
        if upd_item := await self.repository.update_by_id(id, item_dict):
            return upd_item
        raise HTTPException(
                detail="not found",
                status_code=404
            )

    async def delete(self, id: int):
        if item := await self.repository.delete_by_id(id):
            return item
        raise HTTPException(
                detail="not found",
                status_code=404
            )
"""

def gen_service(path, kind: str):
    with open(f"{path}/service.py", "w") as f:
        f.write(TEMPLATE.format(kind=kind.capitalize()))