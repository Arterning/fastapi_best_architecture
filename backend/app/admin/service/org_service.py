#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select
from typing import Sequence, Any

from backend.app.admin.crud.crud_org import org_dao
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session

from backend.app.admin.model import Organization
from backend.app.admin.schema.org import CreateOrgParam, UpdateOrgParam
from backend.utils.build_tree import get_tree_data


class OrgService:
    
    @staticmethod
    async def get(*, pk: int) -> Organization:
        async with async_db_session() as db:
            org = await org_dao.get(db, pk)
            if not org:
                raise errors.NotFoundError(msg='组织不存在')
            return org


        
    @staticmethod
    async def get_docs(pk: int):
        async with async_db_session() as db:
            org = await org_dao.get(db, pk)
            name = org.name
            docs = org.docs
            ocr_res = []
            for doc in docs:
                ocr_res.append(doc.ocr_res)
            return ocr_res, name
    
    @staticmethod
    async def get_children(*, parent_id:int) -> Sequence[Organization]:
        async with async_db_session() as db:
            children = await org_dao.get_children(db, pk)
            return children
    

    @staticmethod
    async def get_org_tree(name: str | None = None, docs: list[int] = None) -> list[dict[str, Any]]:
        async with async_db_session() as db:
            org_list = await org_dao.get_list(db=db, name=name, docs=docs)
            # 默认展示，需要过滤，去掉parent_id为空并且default_show为False的记录
            if not name:
                org_list = [
                    org for org in org_list
                    if org.parent_id or org.default_show
                ]
            tree_data = await get_tree_data(org_list)
            return tree_data


    @staticmethod
    async def get_all(name: str = None) -> Sequence[Organization]:
        async with async_db_session() as db:
            all = await org_dao.get_all(db, name=name)
            return all

    @staticmethod
    async def get_hot_orgs() -> Sequence[Organization]:
        async with async_db_session() as db:
            orgs = await org_dao.get_hot_orgs(db)
            return orgs

    @staticmethod
    async def get_hot_words() -> Sequence[Organization]:
        async with async_db_session() as db:
            words = await org_dao.get_hot_words(db)
            return words

    @staticmethod
    async def get_count() -> int:
        async with async_db_session() as db:
            count = await org_dao.get_count(db)
            return count

    @staticmethod
    async def get_select(*, name: str = None, docs: list[int] = None) -> Select:
        return await org_dao.get_list_select(name=name, docs=docs)

   
    @staticmethod
    async def create(*, obj: CreateOrgParam) -> None:
        async with async_db_session.begin() as db:
           await org_dao.create(db, obj)

    @staticmethod
    async def batch_create(*, objs: list[CreateOrgParam]) -> None:
        async with async_db_session.begin() as db:
            await org_dao.batch_create(db, objs)

    @staticmethod
    async def update(*, pk: int, obj: UpdateOrgParam) -> int:
        async with async_db_session.begin() as db:
            count = await org_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await org_dao.delete(db, pk)
            return count

    @staticmethod
    async def get_by_names(names: list[str]) -> Sequence[Organization]:
        async with async_db_session.begin() as db:
           orgs = await org_dao.get_by_names(db, names) 
           return orgs


org_service = OrgService()