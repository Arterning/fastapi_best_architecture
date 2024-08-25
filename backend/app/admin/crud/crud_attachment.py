#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, and_, delete, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Attachment
from backend.app.admin.schema.attachment import CreateAttachmentParam, UpdateAttachmentParam

class CRUDAttachment(CRUDPlus[Attachment]):
    async def get(self, db: AsyncSession, pk: int) -> Attachment | None:
        return await self.select_model_by_id(db, pk)

    async def get_list(self, name: str = None) -> Select:
        se = select(self.model).order_by(desc(self.model.created_time))
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def get_all(self, db: AsyncSession) -> Sequence[Attachment]:
        return await self.select_models(db)

    async def get_by_name(self, db: AsyncSession, name: str) -> Attachment | None:
        return await self.select_model_by_column(db, 'name', name)

    async def create(self, db: AsyncSession, obj_in: CreateAttachmentParam) -> Attachment:
        attachment = self.model(**obj_in.model_dump())
        db.add(attachment)
        db.flush()
        return attachment

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateAttachmentParam) -> int:
        return await self.update_model(db, pk, obj_in)
    
    async def update_by_ids(self, db: AsyncSession, ids: list[int], person_id: int) -> int:
        valid = await db.execute(update(self.model).where(self.model.id.in_(ids)).values(person_id=person_id))
        invalid = await db.execute(update(self.model)
                         .where(and_(self.model.person_id == person_id, self.model.id.not_in(ids)))
                         .values(person_id=None))
        return valid.rowcount + invalid.rowcount

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        apis = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
        return apis.rowcount


attachment_dao: CRUDAttachment = CRUDAttachment(Attachment)
