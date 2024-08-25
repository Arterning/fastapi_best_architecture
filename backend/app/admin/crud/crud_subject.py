#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, and_, delete, desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.orm import selectinload
from backend.app.admin.model import Subject, Document, Person, Organization
from backend.app.admin.schema.subject import CreateSubjectParam, UpdateSubjectParam


class CRUDSubject(CRUDPlus[Subject]):
    async def get(self, db: AsyncSession, pk: int) -> Subject | None:
        """
        获取 Subject

        :param db:
        :param pk:
        :return:
        """
        where = []
        where.append(self.model.id == pk)
        org = await db.execute(
             select(self.model)
            .options(selectinload(self.model.docs))
            .options(selectinload(self.model.persons))
            .options(selectinload(self.model.orgs))
            .where(*where)
        )
        return org.scalars().first()

    async def get_list(self, name: str = None) -> Select:
        """
        获取 Subject 列表

        :param name:
        :param method:
        :param path:
        :return:
        """
        se = select(self.model).order_by(desc(self.model.created_time))
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def get_all(self, db: AsyncSession) -> Sequence[Subject]:
        """
        获取所有 Subject

        :param db:
        :return:
        """
        return await self.select_models(db)

    async def get_by_name(self, db: AsyncSession, name: str) -> Subject | None:
        """
        通过 name 获取 Subject

        :param db:
        :param name:
        :return:
        """
        return await self.select_model_by_column(db, 'name', name)

    async def create(self, db: AsyncSession, obj_in: CreateSubjectParam) -> None:
        """
        创建 Subject

        :param db:
        :param obj_in:
        :return:
        """
        subject = self.model(name=obj_in.name, detail=obj_in.detail, type=obj_in.type, his=obj_in.his)
        db.add(subject)
        db.flush()

        for i in list(subject.docs):
            subject.docs.remove(i)
        if obj_in.docs:
            doc_list = []
            for doc_id in obj_in.docs:
                doc_list.append(await db.get(Document, doc_id))
            subject.docs.extend(doc_list)

        for i in list(subject.persons):
            subject.persons.remove(i)
        if obj_in.persons:
            person_list = []
            for person_id in obj_in.persons:
                person_list.append(await db.get(Person, person_id))
            subject.persons.extend(person_list)

        for i in list(subject.orgs):
            subject.orgs.remove(i)
        if obj_in.orgs:
            org_list = []
            for org_id in obj_in.orgs:
                org_list.append(await db.get(Organization, org_id))
            subject.orgs.extend(org_list)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateSubjectParam) -> int:
        """
        更新 Subject

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        subject = await self.get(db, pk)
        for i in list(subject.docs):
            subject.docs.remove(i)
        if obj_in.docs:
            doc_list = []
            for doc_id in obj_in.docs:
                doc_list.append(await db.get(Document, doc_id))
            subject.docs.extend(doc_list)
        
        for i in list(subject.persons):
            subject.persons.remove(i)
        if obj_in.persons:
            person_list = []
            for person_id in obj_in.persons:
                person_list.append(await db.get(Person, person_id))
            subject.persons.extend(person_list)

        for i in list(subject.orgs):
            subject.orgs.remove(i)
        if obj_in.orgs:
            org_list = []
            for org_id in obj_in.orgs:
                org_list.append(await db.get(Organization, org_id))
            subject.orgs.extend(org_list)
        
        return await self.update_model(db, pk, {
            "name": obj_in.name,
            "detail": obj_in.detail,
            "type": obj_in.type,
            "his": obj_in.his
        })

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除 Subject

        :param db:
        :param pk:
        :return:
        """
        subjects = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
        return subjects.rowcount

    async def get_count(self, db: AsyncSession) -> int:
        query = await db.execute(select(func.count((self.model.id))))
        return query.scalars().first()

    async def get_hot_subjects(self, db: AsyncSession) -> Sequence[Subject]:
        subquery = (
            select(Subject.id)
            .join(Subject.docs)
            .group_by(Subject.id)
            .order_by(Subject.updated_time.desc(), func.count().desc())
            .limit(10)
        )

        subquery_result = await db.execute(subquery)
        ids = subquery_result.scalars().all()

        if ids and ids is not None:
            query = select(Subject).filter(Subject.id.in_(ids)).order_by(func.field(Subject.id, *ids))
            res = await db.execute(query)
            subjects = res.scalars().all()
            return subjects
        return []
    
    async def get_hot_subject_types(self, db: AsyncSession, hot_subjects: list[Subject]) -> dict:

        hot_subject_ids = [subject.id for subject in hot_subjects]

        query = select(
            Subject.type,
            func.count().label('count'),
            func.sum(func.count()).over().label('total_count')
        ).where(Subject.id.in_(hot_subject_ids)).group_by(Subject.type)

        subquery_result = await db.execute(query)
        result = subquery_result.fetchall()
        
        dict_result = []
        for row in result:
            type_value = row[0]
            count_value = row[1]
            total_count_value = row[2]

            dict_row = {
                'type': type_value,
                'count': count_value,
                'percentage': count_value / total_count_value
            }
            dict_result.append(dict_row)

        return dict_result


    async def get_hot_types(self, db: AsyncSession) -> dict:
        query = select(
            Subject.type,
            func.count().label('count'),
            func.sum(func.count()).over().label('total_count')
        ).group_by(Subject.type)

        subquery_result = await db.execute(query)
        result = subquery_result.fetchall()
        
        dict_result = []
        for row in result:
            type_value = row[0]
            count_value = row[1]
            total_count_value = row[2]

            dict_row = {
                'type': type_value,
                'count': count_value,
                'percentage': count_value / total_count_value
            }
            dict_result.append(dict_row)

        # print(dict_result)
        return dict_result



    
    async def get_or_create_by_name(self, db: AsyncSession, name: str) -> Subject | None:
        """
        通过 name 获取 Subject 或创建

        :param db:
        :param name:
        :return:
        """
        subject = await self.get_by_name(db, name)
        if subject:
            return subject
        subject = self.model(name=name, detail='')
        db.add(subject)
        db.flush()
        return subject
    

subject_dao: CRUDSubject = CRUDSubject(Subject)
