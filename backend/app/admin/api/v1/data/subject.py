#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.admin.schema.subject import CreateSubjectParam, GetSubjectListDetails, GetSubjectList, UpdateSubjectParam
from backend.app.admin.service.subject_service import subject_service
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db_mysql import CurrentSession
from backend.utils.serializers import select_as_dict


router = APIRouter()


@router.get('/all', summary='获取所有接口', dependencies=[DependsJwtAuth])
async def get_all_subjects() -> ResponseModel:
    data = await subject_service.get_all()
    data = [GetSubjectList(**await select_as_dict(subject)) for subject in data]
    return await response_base.success(data=data)


@router.get('/{pk}', summary='获取接口详情', dependencies=[DependsJwtAuth])
async def get_subject(pk: Annotated[int, Path(...)]) -> ResponseModel:
    subject = await subject_service.get(pk=pk)
    docs = [dict(id=doc.id, title=doc.title) for doc in subject.docs]
    subject_data = await select_as_dict(subject)
    subject_data.pop('docs', None)
    data = GetSubjectListDetails(**subject_data, docs=docs)
    if data.his is None:
        data.his = []
    return await response_base.success(data=data)


@router.get(
    '',
    summary='（模糊条件）分页获取所有接口',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_subjects(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
) -> ResponseModel:
    subject_select = await subject_service.get_select(name=name)
    page_data = await paging_data(db, subject_select, GetSubjectList)
    return await response_base.success(data=page_data)


@router.post(
    '',
    summary='创建接口',
    dependencies=[
        Depends(RequestPermission('sys:subject:add')),
        DependsRBAC,
    ],
)
async def create_subject(obj: CreateSubjectParam) -> ResponseModel:
    await subject_service.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新接口',
    dependencies=[
        Depends(RequestPermission('sys:subject:edit')),
        DependsRBAC,
    ],
)
async def update_subject(pk: Annotated[int, Path(...)], obj: UpdateSubjectParam) -> ResponseModel:
    count = await subject_service.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '',
    summary='（批量）删除接口',
    dependencies=[
        Depends(RequestPermission('sys:subject:del')),
        DependsRBAC,
    ],
)
async def delete_subject(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await subject_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
