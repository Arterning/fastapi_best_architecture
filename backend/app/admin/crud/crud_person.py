#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, and_, func,  delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.orm import selectinload
from backend.app.admin.model import Person, Document, Organization
from backend.app.admin.schema.person import CreatePersonParam, UpdatePersonParam


class CRUDPerson(CRUDPlus[Person]):
    async def get(self, db: AsyncSession, pk: int) -> Person | None:
        where = []
        where.append(self.model.id == pk)
        person = await db.execute(
             select(self.model)
            .options(selectinload(self.model.docs))
            .options(selectinload(self.model.orgs))
            .options(selectinload(self.model.attachments))
            .where(*where)
        )
        return person.scalars().first()

    async def get_list(self, name: str = None, job: str = None, docs: list[int] = None) -> Select:
        se = select(self.model).order_by(desc(self.model.created_time))
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if docs:
            se = se.join(self.model.docs)
            where_list.append(self.model.docs.any(Document.id.in_(docs)))
        if where_list:
            se = se.options(selectinload(self.model.docs)).where(and_(*where_list))
        return se

    async def get_hot_persons(self, db: AsyncSession) -> Sequence[Person]:
        subquery = (
            select(Person.id)
            .join(Person.docs)
            .group_by(Person.id)
            .order_by(Person.updated_time.desc(), func.count().desc())
            .limit(10)
        )

        # print(subquery)
        subquery_result = await db.execute(subquery)
        ids = subquery_result.scalars().all()

        if ids and ids is not None:
        
            query = select(Person).options(selectinload(self.model.attachments)).filter(Person.id.in_(ids)).order_by(func.field(Person.id, *ids))

            res = await db.execute(query)
            persons = res.scalars().all()

            return persons
        
        return []

    async def get_hot_words(self, db: AsyncSession) -> Sequence[dict]:
        subquery = (
            select(
                Person.id,
                Person.name,
                func.count().label('count')
            )
            .join(Person.docs)
            .group_by(Person.id)
            .order_by(Person.updated_time.desc(), func.count().desc())
            .limit(20)
        )
        result = await db.execute(subquery)
        hot_persons = result.fetchall()
        result = [{"id": person[0], "name": person[1], "value": person[2], "type": "Person"} for person in hot_persons]
        return result


    async def get_all(self, db: AsyncSession, name: str = None) -> Sequence[Person]:
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        persons = await db.execute(
             select(self.model)
            .where(*where_list)
            .order_by(self.model.created_time.desc())
            .limit(500)
        )
        return persons.scalars()

    async def get_count(self, db: AsyncSession) -> int:
        query = await db.execute(select(func.count((self.model.id))))
        return query.scalars().first()

    async def get_by_name(self, db: AsyncSession, name: str) -> Person | None:
        return await self.select_model_by_column(db, 'name', name)
    

    async def batch_create(self, db: AsyncSession, objs: list[CreatePersonParam]) -> None:
        for obj_in in objs:
            person = await self.get_by_name(db, obj_in.name)
            if person:
                await self.update_model(db, person.id, {
                    "job": obj_in.job,
                    "org_name":obj_in.org_name
                })
            else:
                person = self.model(name=obj_in.name, detail=obj_in.detail, birth_date=obj_in.birth_date)
                db.add(person)
        db.flush()


    async def create(self, db: AsyncSession, obj_in: CreatePersonParam) -> Person:
        person = self.model(name=obj_in.name, detail=obj_in.detail, birth_date=obj_in.birth_date,icon=obj_in.icon)
        db.add(person)
        db.flush()
        
        if obj_in.docs is not None:
            for i in list(person.docs):
                person.docs.remove(i)
            doc_list = []
            for doc_id in obj_in.docs:
                doc_list.append(await db.get(Document, doc_id))
            person.docs.extend(doc_list)
        
        if obj_in.orgs is not None:
            for i in list(person.orgs):
                person.orgs.remove(i)
            org_list = []
            for org_id in obj_in.orgs:
                org_list.append(await db.get(Organization, org_id))
            person.orgs.extend(org_list)
        return person
        

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdatePersonParam) -> int:
        person = await self.get(db, pk)
        for i in list(person.docs):
            person.docs.remove(i)
        doc_list = []
        for doc_id in obj_in.docs:
            doc_list.append(await db.get(Document, doc_id))
        person.docs.extend(doc_list)

        for i in list(person.orgs):
            person.orgs.remove(i)
        org_list = []
        for org_id in obj_in.orgs:
            org_list.append(await db.get(Organization, org_id))
        person.orgs.extend(org_list)

        return await self.update_model(db, pk, {
            "name": obj_in.name,
            "detail": obj_in.detail,
            "icon": obj_in.icon,
            "birth_date": obj_in.birth_date,
        })

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        apis = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
        return apis.rowcount

    async def get_by_names(self, db: AsyncSession, names: list[str]) -> Sequence[Person]:
        se = select(self.model).where(self.model.name.in_(names))
        persons = await db.execute(se)
        return persons.scalars().all()

        
person_dao: CRUDPerson = CRUDPerson(Person)
