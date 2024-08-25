#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase
from backend.app.admin.schema.person import GetPersonListDetails
from backend.app.admin.schema.org import GetOrgListDetails


class SubjectSchemaBase(SchemaBase):
    name: str
    type: str | None = None
    detail: str | None = None


class CreateSubjectParam(SubjectSchemaBase):
    docs: list[int] | None = None
    persons: list[int] | None = None
    orgs:  list[int] | None = None
    his: list[dict] | None = None
    pass

class UpdateSubjectParam(SubjectSchemaBase):
    docs: list[int] | None = None
    persons: list[int] | None = None
    orgs:  list[int] | None = None
    his: list[dict] | None = None
    pass

class GetSubjectList(SubjectSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None


class GetSubjectListDetails(SubjectSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    docs: list[dict]
    persons: list[GetPersonListDetails]
    orgs: list[GetOrgListDetails]
    his: list[dict] | None = None
    created_time: datetime
    updated_time: datetime | None = None