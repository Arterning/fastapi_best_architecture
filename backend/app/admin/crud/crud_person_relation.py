#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, and_, func,  delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.orm import selectinload
from backend.app.admin.model import PersonRelation


class CRUDPersonRelation(CRUDPlus[PersonRelation]):

    async def get_relations(self, db: AsyncSession, pk: int) -> Sequence[PersonRelation] | None:
        where = []
        where.append(self.model.person_id == pk)
        person = await db.execute(
             select(self.model)
            .where(*where)
        )
        return person.scalars().all()
    
person_relation_dao: CRUDPersonRelation = CRUDPersonRelation(PersonRelation)    