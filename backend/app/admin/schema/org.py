#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, date

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class OrgSchemaBase(SchemaBase):
    name: str
    parent_id: int | None = Field(default=None, description='部门父级ID')
    detail: str | None = None


class CreateOrgParam(OrgSchemaBase):
    docs: list[int] | None = None
    pass

class UpdateOrgParam(OrgSchemaBase):
    docs: list[int] | None = None
    persons: list[int] | None = None
    default_show: bool  = False
    pass

class GetOrgListDetails(OrgSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None

class GetOrgDocListDetails(GetOrgListDetails):
    docs: list[dict]
    persons: list[dict]
    parent: dict | None
    children: list[dict]
    activity: list[dict] | None
    default_show: bool = False