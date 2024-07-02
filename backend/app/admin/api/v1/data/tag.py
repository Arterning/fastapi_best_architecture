#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.tag import CreateTagParam, GetTagListDetails, UpdateTagParam
from backend.app.admin.service.tag_service import tag_service
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db_mysql import CurrentSession
from backend.utils.serializers import select_as_dict

router = APIRouter()


@router.get('/all', summary='获取所有接口', dependencies=[DependsJwtAuth])
async def get_all_tags(request: Request) -> ResponseModel:
    user_id = request.user.id
    tags = await tag_service.get_all(user_id)
    data = [GetTagListDetails(**await select_as_dict(tag)) for tag in tags]
    return await response_base.success(data=data)


@router.get('/{pk}', summary='获取接口详情', dependencies=[DependsJwtAuth])
async def get_tag(pk: Annotated[int, Path(...)]) -> ResponseModel:
    tag = await tag_service.get(pk=pk)
    data = GetTagListDetails(**await select_as_dict(tag))
    return await response_base.success(data=data)


@router.get(
    '',
    summary='（模糊条件）分页获取所有接口',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_tags(
    db: CurrentSession,
    request: Request,
    name: Annotated[str | None, Query()] = None,
) -> ResponseModel:
    user_id = request.user.id
    tag_select = await tag_service.get_select(name=name, user_id=user_id)
    page_data = await paging_data(db, tag_select, GetTagListDetails)
    return await response_base.success(data=page_data)


@router.post(
    '',
    summary='创建接口',
    dependencies=[
        Depends(RequestPermission('sys:tag:add')),
        DependsRBAC,
    ],
)
async def create_tag(request: Request, obj: CreateTagParam) -> ResponseModel:
    user_id = request.user.id
    await tag_service.create(obj=obj, user_id=user_id)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新接口',
    dependencies=[
        Depends(RequestPermission('sys:tag:edit')),
        DependsRBAC,
    ],
)
async def update_tag(request: Request, pk: Annotated[int, Path(...)], obj: UpdateTagParam) -> ResponseModel:
    user_id = request.user.id
    count = await tag_service.update(pk=pk, obj=obj, user_id=user_id)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '',
    summary='（批量）删除接口',
    dependencies=[
        Depends(RequestPermission('sys:tag:del')),
        DependsRBAC,
    ],
)
async def delete_tag(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await tag_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
