#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, and_, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Tag
from backend.app.admin.schema.tag import CreateTagParam, UpdateTagParam


class CRUDTag(CRUDPlus[Tag]):
    async def get(self, db: AsyncSession, pk: int) -> Tag | None:
        """
        获取 Tag

        :param db:
        :param pk:
        :return:
        """
        return await self.select_model_by_id(db, pk)

    async def get_list(self, name: str = None, user_id: int = None) -> Select:
        """
        获取 Tag 列表

        :param name:
        :param method:
        :param path:
        :return:
        """
        se = select(self.model).order_by(desc(self.model.created_time))
        where_list = []
        where_list.append(self.model.user_id==user_id)
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def get_all(self, db: AsyncSession, user_id: int) -> Sequence[Tag]:
        """
        获取所有 Tag

        :param db:
        :return:
        """
        query = await db.execute(select(self.model).where(self.model.user_id == user_id))
        return query.scalars().all()

    async def get_by_name(self, db: AsyncSession, name: str, user_id: int) -> Tag | None:
        """
        通过 name 获取 Tag

        :param db:
        :param name:
        :return:
        """
        query = await db.execute(select(self.model).where(and_(self.model.name == name, self.model.user_id == user_id)))
        return query.scalars().first()

    async def get_or_create_by_name(self, db: AsyncSession, name: str, user_id: int) -> Tag | None:
        """
        通过 name 获取 Tag 或创建

        :param db:
        :param name:
        :return:
        """
        tag = await self.get_by_name(db, name, user_id)
        if tag:
            return tag
        param = CreateTagParam(name=name)
        tag = self.model(**param.model_dump(), user_id=user_id)
        db.add(tag)
        db.flush()
        return tag


    async def create(self, db: AsyncSession, obj_in: CreateTagParam, user_id: int) -> None:
        """
        创建 Tag

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in, user_id=user_id)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateTagParam, user_id: int) -> int:
        """
        更新 Tag

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除 Tag

        :param db:
        :param pk:
        :return:
        """
        tags = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
        return tags.rowcount


tag_dao: CRUDTag = CRUDTag(Tag)
