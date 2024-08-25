#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.admin.crud.crud_attachment import attachment_dao
from backend.app.admin.model import Attachment
from backend.app.admin.schema.attachment import CreateAttachmentParam, UpdateAttachmentParam
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session


class AttachmentService:
    @staticmethod
    async def get(*, pk: int) -> Attachment:
        async with async_db_session() as db:
            api = await attachment_dao.get(db, pk)
            if not api:
                raise errors.NotFoundError(msg='资源不存在')
            return api

    @staticmethod
    async def get_select(*, name: str = None, method: str = None, path: str = None) -> Select:
        return await attachment_dao.get_list(name=name, method=method, path=path)

    @staticmethod
    async def get_all() -> Sequence[Attachment]:
        async with async_db_session() as db:
            apis = await attachment_dao.get_all(db)
            return apis

    @staticmethod
    async def create(*, obj: CreateAttachmentParam) -> Attachment:
        async with async_db_session.begin() as db:
            return await attachment_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateAttachmentParam) -> int:
        async with async_db_session.begin() as db:
            count = await attachment_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await attachment_dao.delete(db, pk)
            return count


attachment_service = AttachmentService()
