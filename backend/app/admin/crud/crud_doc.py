#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select,  and_, or_,  func, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.orm import selectinload, aliased

from backend.app.admin.model import Document, Tag
from backend.app.admin.schema.doc import CreateDocParam, UpdateDocParam


class CRUDDoc(CRUDPlus[Document]):

    async def get(self, db: AsyncSession, pk: int) -> Document | None:
        """
        获取 Document

        :param db:
        :param pk:
        :return:
        """
        where = []
        where.append(self.model.id == pk)
        doc = await db.execute(
             select(self.model)
            .options(selectinload(self.model.tags))
            .where(*where)
        )
        return doc.scalars().first()

    async def get_all(self, db: AsyncSession, title: str = None) -> Sequence[Document]:
        """
        获取所有文档
        :param db:
        :return:
        """
        se = select(self.model).order_by(desc(self.model.created_time))
        where_list = []
        if title:
            where_list.append(self.model.title.like(f'%{title}%'))
        docs = await db.execute(
             select(self.model)
            .where(*where_list)
        )
        return docs.scalars()

    async def get_count(self, db: AsyncSession) -> int:
        query = await db.execute(select(func.count((self.model.id))))
        return query.scalars().first()


    async def get_list(self, ids: list[int], title: list[str] = None, start_time: str = None, end_time :str = None, tags: list[int] = None) -> Select:
        """
        获取列表
        """
        se = (
            select(self.model)
                .options(selectinload(self.model.tags))
                .order_by(desc(self.model.created_time))
        )
        where_list = []
        if ids is not None:
            where_list.append(self.model.id.in_(ids))
        if title:
            title_filters = [self.model.title.like(f'%{t}%') for t in title]
            where_list.extend(title_filters)
        if start_time:
            where_list.append(self.model.created_time >= start_time)
        if end_time:
            where_list.append(self.model.created_time <= end_time)
        if tags:
            se = se.join(self.model.tags)
            where_list.append(self.model.tags.any(Tag.id.in_(tags)))
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def get_by_title(self, db: AsyncSession, title: str) -> Document | None:
        """
        通过 title 获取

        :param db:
        :param name:
        :return:
        """
        return await self.select_model_by_column(db, 'title', title)

    async def get_by_uuid(self, db: AsyncSession, uuid: str) -> Document | None:
        """
        通过 uuid 获取

        :param db:
        :param name:
        :return:
        """
        return await self.select_model_by_column(db, 'uuid', uuid)
    

    async def create(self, db: AsyncSession, obj_in: CreateDocParam) -> None:
        """
        创建文档
        """
        # dump =  obj_in.model_dump()
        # print(dump)
        doc = self.model(title=obj_in.title,content=obj_in.content,
                            subject=obj_in.subject, url=obj_in.url, uuid=obj_in.uuid)
        db.add(doc)
        db.flush()
        return doc
        

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateDocParam) -> int:
        """
        更新
        """
        # doc = await self.get(db, pk)
        # for i in list(doc.persons):
        #     doc.persons.remove(i)
        # person_list = []
        # for person_id in obj_in.persons:
        #     person_list.append(await db.get(Person, person_id))
        # doc.persons.extend(person_list)

        return await self.update_model(db, pk, {
            "title": obj_in.title,
            "content": obj_in.content,
            "subject": obj_in.subject,
        })


    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除
        :param db:
        :param pk:
        :return:
        """
        res = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
        return res.rowcount

    async def get_by_ids(self, db: AsyncSession, pk: list[int]) -> Sequence[Document]:
        res = await db.execute(select(self.model).where(self.model.id.in_(pk)))
        return res.scalars().all()

doc_dao: CRUDDoc = CRUDDoc(Document)