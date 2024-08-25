#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.admin.crud.crud_subject import subject_dao
from backend.app.admin.model import Subject
from backend.app.admin.schema.subject import CreateSubjectParam, UpdateSubjectParam
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session


class SubjectService:
    @staticmethod
    async def get(*, pk: int) -> Subject:
        async with async_db_session() as db:
            subject = await subject_dao.get(db, pk)
            if not subject:
                raise errors.NotFoundError(msg='接口不存在')
            return subject
        
    @staticmethod
    async def get_docs(pk: int):
        async with async_db_session() as db:
            subject = await subject_dao.get(db, pk)
            name = subject.name
            docs = subject.docs
            ocr_res = []
            for doc in docs:
                ocr_res.append(doc.ocr_res)
            return ocr_res, name

    @staticmethod
    async def get_select(*, name: str = None) -> Select:
        return await subject_dao.get_list(name=name)

    @staticmethod
    async def get_all() -> Sequence[Subject]:
        async with async_db_session() as db:
            subjects = await subject_dao.get_all(db)
            return subjects

    @staticmethod
    async def create(*, obj: CreateSubjectParam) -> None:
        async with async_db_session.begin() as db:
            subject = await subject_dao.get_by_name(db, obj.name)
            if subject:
                raise errors.ForbiddenError(msg='接口已存在')
            await subject_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateSubjectParam) -> int:
        async with async_db_session.begin() as db:
            count = await subject_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await subject_dao.delete(db, pk)
            return count

    @staticmethod
    async def get_count() -> int:
        async with async_db_session() as db:
            count = await subject_dao.get_count(db)
            return count

    @staticmethod
    async def get_hot_subjects() -> Sequence[Subject]:
        async with async_db_session() as db:
            subs = await subject_dao.get_hot_subjects(db)
            return subs

    @staticmethod
    async def get_hot_types() -> dict:
        async with async_db_session() as db:
            hot_types = await subject_dao.get_hot_types(db)
            return hot_types
    
    @staticmethod
    async def get_hot_subject_types(hot_subjects: list[Subject]) -> dict:
        async with async_db_session() as db:
            hot_types = await subject_dao.get_hot_subject_types(db, hot_subjects)
            return hot_types
        
    @staticmethod
    async def get_or_create_by_name(name: str = None) -> Subject:
        async with async_db_session.begin() as db:
            subject = await subject_dao.get_or_create_by_name(db, name)
            return subject
                
subject_service = SubjectService()
