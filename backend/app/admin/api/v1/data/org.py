#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.admin.schema.org import CreateOrgParam, GetOrgListDetails, UpdateOrgParam, GetOrgDocListDetails
from backend.app.admin.service.org_service import org_service
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db_mysql import CurrentSession
from backend.utils.serializers import select_as_dict

router = APIRouter()


@router.get('/all', summary='获取所有接口', dependencies=[DependsJwtAuth])
async def get_all_orgs(name: Annotated[str | None, Query()] = None) -> ResponseModel:
    orgs = await org_service.get_all(name=name)
    data = [GetOrgListDetails(** await select_as_dict(org)) for org in orgs]
    return await response_base.success(data=data)

@router.get(
    '/tree',
    summary='获取所有组织展示树',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_tree_orgs(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    docs: Annotated[list[int] | None, Query()] = None
) -> ResponseModel:
    tree = await org_service.get_org_tree(name=name, docs=docs)
    return await response_base.success(data=tree)



@router.get('/{pk}', summary='获取接口详情', dependencies=[DependsJwtAuth])
async def get_org(pk: Annotated[int, Path(...)]) -> ResponseModel:
    org = await org_service.get(pk=pk)
    docs = [dict(id=doc.id, title=doc.title) for doc in org.docs]
    persons = [dict(id=person.id, name=person.name, icon=person.icon) for person in org.persons]
    children = [dict(id=child.id, name=child.name) for child in org.children]
    parent = None
    if org.parent is not None:
        parent = dict(id=org.parent_id, name=org.parent.name)
    data = GetOrgDocListDetails(id=org.id, name=org.name, created_time=org.created_time,
                                    detail=org.detail, docs=docs, persons=persons,default_show=org.default_show,
                                    children=children, parent=parent, activity=org.activity)
    return await response_base.success(data=data)



@router.get(
    '',
    summary='（模糊条件）分页获取所有接口',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_orgs(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    docs: Annotated[list[int] | None, Query()] = None
) -> ResponseModel:
    se = await org_service.get_select(name=name, docs=docs)
    page_data = await paging_data(db, se, GetOrgListDetails)
    return await response_base.success(data=page_data)


@router.post(
    '',
    summary='创建接口',
)
async def create_org(obj: CreateOrgParam) -> ResponseModel:
    await org_service.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新接口',
)
async def update_org(pk: Annotated[int, Path(...)], obj: UpdateOrgParam) -> ResponseModel:
    count = await org_service.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '',
    summary='（批量）删除接口',
)
async def delete_org(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await org_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
