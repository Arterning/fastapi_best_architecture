#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, and_, or_, func,  delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.orm import selectinload
from backend.app.admin.model import Organization, Document, Person
from backend.app.admin.schema.org import CreateOrgParam, UpdateOrgParam


class CRUDOrg(CRUDPlus[Organization]):
    async def get(self, db: AsyncSession, pk: int) -> Organization | None:
        where = []
        where.append(self.model.id == pk)
        org = await db.execute(
             select(self.model)
            .options(selectinload(self.model.docs))
            .options(selectinload(self.model.persons))
            .options(selectinload(self.model.parent))
            .options(selectinload(self.model.children))
            .where(*where)
        )
        return org.scalars().first()
    
    async def get_children(self, db: AsyncSession, parent_id: int) -> Sequence[Organization]:
        se = select(self.model).order_by(desc(self.model.created_time))
        where_list = []
        where_list.append(self.model.parent_id == parent_id)
        se = se.where(and_(*where_list))
        children = await db.execute(se)
        return children.scalars().all()

    async def get_list_select(self, name: str = None, docs: list[int] = None) -> Select:
        se = select(self.model).order_by(desc(self.model.created_time))
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if docs:
            se = se.join(self.model.docs)
            where_list.append(self.model.docs.any(Document.id.in_(docs)))            
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def get_list(self, db: AsyncSession, name: str = None, docs: list[int] = None) -> Sequence[Organization]:
        se = select(self.model).order_by(desc(self.model.created_time))
        where_list = []
        conditions = []
        if name:
            conditions.append(self.model.name.like(f'%{name}%'))
        if docs:
            se = se.join(self.model.docs)
            conditions.append(self.model.docs.any(Document.id.in_(docs)))     
        if conditions:
            org_select = await db.execute(se.where(and_(*conditions)))
            org_likes = org_select.scalars().all()
            # find match condition orgs and it's parent org
            where_list.append(or_(*conditions, self.model.id.in_([org.parent_id for org in org_likes]))) 
        if where_list:
            se = se.where(and_(*where_list))
        orgs = await db.execute(se)
        return orgs.scalars().all()

    async def get_all(self, db: AsyncSession, name: str = None) -> Sequence[Organization]:
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        orgs = await db.execute(
             select(self.model)
            .where(*where_list)
            .order_by(self.model.created_time.desc())
            .limit(500)
        )
        return orgs.scalars()

    async def get_hot_words(self, db: AsyncSession) -> Sequence[dict]:
        subquery = (
            select(
                Organization.id,
                Organization.name,
                func.count().label('count')
            )
            .join(Organization.docs, isouter=True)
            .group_by(Organization.id)
            .order_by(Organization.updated_time.desc(), func.count().desc())
            .limit(20)
        )
        result = await db.execute(subquery)
        hot_orgs = result.fetchall()
        result = [{"id": org[0], "name": org[1], "value": org[2], "type": "Org"} for org in hot_orgs]
        return result

    async def get_hot_orgs(self, db: AsyncSession) -> Sequence[Organization]:
        subquery = (
            select(Organization.id)
            .join(Organization.docs)
            .group_by(Organization.id)
            .order_by(Organization.updated_time.desc(), func.count().desc())
            .limit(10)
        )

        # print(subquery)
        subquery_result = await db.execute(subquery)
        org_ids = subquery_result.scalars().all()
        # print("Subquery Result:", org_ids)

        if org_ids and org_ids is not None:
            query = select(Organization).filter(Organization.id.in_(org_ids)).order_by(func.field(Organization.id, *org_ids))
            # print(query)
            res = await db.execute(query)
            orgs = res.scalars().all()
            # print("Orgs", orgs)
            return orgs
        
        return []

    async def get_count(self, db: AsyncSession) -> int:
        query = await db.execute(select(func.count((self.model.id))))
        return query.scalars().first()

    async def get_by_name(self, db: AsyncSession, name: str) -> Organization | None:
        return await self.select_model_by_column(db, 'name', name)

    async def batch_create(self, db: AsyncSession, objs: list[CreateOrgParam]) -> None:
        for obj_in in objs:
            org = await self.get_by_name(db, obj_in.name)
            if org:
                return
            org = self.model(name=obj_in.name, detail=obj_in.detail, parent_id=obj_in.parent_id)
            db.add(org)
        db.flush()

    async def create(self, db: AsyncSession, obj_in: CreateOrgParam) -> None:
        org = self.model(name=obj_in.name, detail=obj_in.detail, parent_id=obj_in.parent_id)
        db.add(org)
        db.flush()
        for i in list(org.docs):
            org.docs.remove(i)
        doc_list = []
        for doc_id in obj_in.docs:
            doc_list.append(await db.get(Document, doc_id))
        org.docs.extend(doc_list)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateOrgParam) -> int:
        org = await self.get(db, pk)

        if obj_in.docs is not None:
            for i in list(org.docs):
                org.docs.remove(i)
            doc_list = []
            for doc_id in obj_in.docs:
                doc_list.append(await db.get(Document, doc_id))
            org.docs.extend(doc_list)

        if obj_in.persons is not None:
            for i in list(org.persons):
                org.persons.remove(i)
            person_list = []
            for person_id in obj_in.persons:
                person_list.append(await db.get(Person, person_id))
            org.persons.extend(person_list)

        return await self.update_model(db, pk, {
            "name": obj_in.name,
            "detail": obj_in.detail,
            "parent_id": obj_in.parent_id,
            "default_show": obj_in.default_show,
        })

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        apis = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
        return apis.rowcount

    async def get_by_names(self, db: AsyncSession, names: list[str]) -> Sequence[Organization]:
        se = select(self.model).where(self.model.name.in_(names))
        orgs = await db.execute(se)
        return orgs.scalars().all()


org_dao: CRUDOrg = CRUDOrg(Organization)
