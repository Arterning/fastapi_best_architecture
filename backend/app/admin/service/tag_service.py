#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.admin.crud.crud_tag import tag_dao
from backend.app.admin.model import Tag
from backend.app.admin.schema.tag import CreateTagParam, UpdateTagParam
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session


class TagService:
    @staticmethod
    async def get(*, pk: int) -> Tag:
        async with async_db_session() as db:
            tag = await tag_dao.get(db, pk)
            if not tag:
                raise errors.NotFoundError(msg='接口不存在')
            return tag

    @staticmethod
    async def get_select(*, name: str = None, user_id: int) -> Select:
        return await tag_dao.get_list(name=name, user_id=user_id)

    @staticmethod
    async def get_all(user_id: int) -> Sequence[Tag]:
        async with async_db_session() as db:
            tags = await tag_dao.get_all(db, user_id)
            return tags

    @staticmethod
    async def create(*, obj: CreateTagParam, user_id: int) -> None:
        async with async_db_session.begin() as db:
            tag = await tag_dao.get_by_name(db, obj.name, user_id)
            if tag:
                raise errors.ForbiddenError(msg='标签已存在')
            await tag_dao.create(db, obj, user_id)

    @staticmethod
    async def update(*, pk: int, obj: UpdateTagParam, user_id: int) -> int:
        async with async_db_session.begin() as db:
            count = await tag_dao.update(db, pk, obj, user_id)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await tag_dao.delete(db, pk)
            return count


tag_service = TagService()
