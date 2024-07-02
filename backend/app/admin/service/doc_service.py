#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select, select, and_
from typing import Sequence

from backend.app.admin.crud.crud_doc import doc_dao
from backend.app.admin.crud.crud_tag import tag_dao
from backend.app.admin.crud.crud_user import user_dao
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session

from backend.app.admin.model import Document, User
from backend.app.admin.schema.doc import CreateDocParam, UpdateDocParam
from backend.app.admin.model.sys_user_doc import sys_user_doc


class DocService:
    
    @staticmethod
    async def get(*, pk: int) -> Document:
        async with async_db_session() as db:
            doc = await doc_dao.get(db, pk)
            if not doc:
                raise errors.NotFoundError(msg='文档不存在')
            return doc

    @staticmethod
    async def get_by_uuid(*, uuid: str) -> Document:
        async with async_db_session() as db:
            doc = await doc_dao.get_by_uuid(db, uuid)
            if not doc:
                raise errors.NotFoundError(msg='文档不存在')
            return doc

    @staticmethod
    async def get_all(title: str = None) -> Sequence[Document]:
        async with async_db_session() as db:
            all = await doc_dao.get_all(db, title=title)
            return all
    
    @staticmethod
    async def get_count() -> int:
        async with async_db_session() as db:
            count = await doc_dao.get_count(db)
            return count
    
    @staticmethod
    async def get_by_ids(*, pk: list[int]) -> Sequence[Document]:
        async with async_db_session() as db:
            all = await doc_dao.get_by_ids(db, pk)
            return all

    @staticmethod
    async def get_select(*, ids: list[int], title: list[str] = None, rangeValue: list[str], tags: list[int] = None) -> Select:
        start_time = rangeValue[0]
        end_time = rangeValue[1]
        return await doc_dao.get_list(ids=ids, title=title, start_time=start_time, end_time=end_time, tags=tags)

   
    @staticmethod
    async def create(*, obj: CreateDocParam, user_id: int) -> Document:
        async with async_db_session.begin() as db:
           doc = await doc_dao.create(db, obj)
           for i in list(doc.tags):
                doc.tags.remove(i)
           tag_list = []
           for tag_name in obj.tags:
                tag = await tag_dao.get_or_create_by_name(db, tag_name, user_id)
                tag_list.append(tag)
           doc.tags.extend(tag_list)
           return doc

    @staticmethod
    async def update(*, pk: int, obj: UpdateDocParam, user_id: int) -> int:
        async with async_db_session.begin() as db:
            count = await doc_dao.update(db, pk, obj)
            doc = await doc_dao.get(db, pk)
            for i in list(doc.tags):
                doc.tags.remove(i)
            tag_list = []
            for tag_name in obj.tags:
                tag = await tag_dao.get_or_create_by_name(db, tag_name, user_id)
                tag_list.append(tag)
            doc.tags.extend(tag_list)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await doc_dao.delete(db, pk)
            return count

    # @staticmethod
    # async def relate_person(doc_id: int, person_id: int) -> None:
    #      async with async_db_session() as db:
    #         insert_stmt = sys_doc_person.insert().values(doc_id=doc_id, person_id=person_id)
    #         await db.execute(insert_stmt)
    #         await db.commit()

    @staticmethod
    async def get_follow_doc_ids(user_id: int) -> list[int]:
        async with async_db_session() as db:
            stmt = select(sys_user_doc.c.doc_id).where(sys_user_doc.c.user_id == user_id)
            result = await db.execute(stmt)
            follow_doc_ids = [row[0] for row in result]
            return follow_doc_ids

    @staticmethod
    async def follow_doc(user_id: int, doc_id: int) -> None:
        async with async_db_session() as db:
            # Check if the user is already following the document
            se = await db.execute(select(sys_user_doc)
                                    .where(
                                        sys_user_doc.c.user_id == user_id,
                                        sys_user_doc.c.doc_id == doc_id
                                    ))
            existing_doc = se.scalars().first()
            if existing_doc:
                return

            # Create a new row in sys_user_doc
            insert_stmt = sys_user_doc.insert().values(user_id=user_id, doc_id=doc_id)
            await db.execute(insert_stmt)
            await db.commit()
            
    @staticmethod
    async def unfollow_doc(user_id: int, doc_id: int) -> None:
        async with async_db_session() as db:
            # Delete the row from sys_user_doc if the user is following the document
            delete_stmt = sys_user_doc.delete().where(
                and_(sys_user_doc.c.user_id == user_id, sys_user_doc.c.doc_id == doc_id)
            )
            await db.execute(delete_stmt)
            await db.commit()


doc_service = DocService()