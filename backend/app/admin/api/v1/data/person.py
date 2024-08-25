#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.admin.schema.person import CreatePersonParam, GetPersonListDetails, UpdatePersonParam, GetPersonDocListDetails
from backend.app.admin.service.person_service import person_service
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db_mysql import CurrentSession
from backend.utils.serializers import select_as_dict

router = APIRouter()


@router.get('/all', summary='获取所有接口', dependencies=[DependsJwtAuth])
async def get_all_persons(name: Annotated[str | None, Query()] = None) -> ResponseModel:
    persons = await person_service.get_all(name=name)
    data = [GetPersonListDetails(**await select_as_dict(person)) for person in persons]
    return await response_base.success(data=data)


@router.get('/{pk}', summary='获取接口详情', dependencies=[DependsJwtAuth])
async def get_person(pk: Annotated[int, Path(...)]) -> ResponseModel:
    person = await person_service.get(pk=pk)
    docs = [dict(id=doc.id, title=doc.title) for doc in person.docs]
    orgs = [dict(id=org.id, name=org.name) for org in person.orgs]
    attachments = [dict(id=a.id, name=a.name, obj_name=a.obj_name, url=a.url) for a in person.attachments]
    relation_json, relation_list, persons = await person_service.get_relations(person_id=pk, person_name=person.name)
    data = GetPersonDocListDetails(id=person.id, name=person.name,relation_json=relation_json,relations=relation_list,
                        birth_date=person.birth_date,activity=person.activity,persons=persons,created_time=person.created_time, 
                        detail=person.detail, docs=docs, orgs=orgs, attachments=attachments)
    return await response_base.success(data=data)


@router.get(
    '',
    summary='（模糊条件）分页获取所有接口',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_persons(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    job: Annotated[str | None, Query()] = None,
    docs: Annotated[list[int] | None, Query()] = None
) -> ResponseModel:
    person_select = await person_service.get_select(name=name, job=job, docs=docs)
    page_data = await paging_data(db, person_select, GetPersonListDetails)
    return await response_base.success(data=page_data)


@router.post(
    '',
    summary='创建接口',
)
async def create_person(obj: CreatePersonParam) -> ResponseModel:
    await person_service.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新接口',
)
async def update_person(pk: Annotated[int, Path(...)], obj: UpdatePersonParam) -> ResponseModel:
    count = await person_service.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '',
    summary='（批量）删除接口',
)
async def delete_person(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await person_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
