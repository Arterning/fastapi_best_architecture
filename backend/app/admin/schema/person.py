#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, date

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class PersonSchemaBase(SchemaBase):
    name: str
    icon: str | None = None
    birth_date: date | None = None
    detail: str | None = None


class CreatePersonParam(PersonSchemaBase):
    docs: list[int] | None = None
    orgs: list[int] | None = None
    relations: list[dict] | None = None
    attachments: list[dict] | None = None
    pass

class UpdatePersonParam(PersonSchemaBase):
    docs: list[int] | None = None
    orgs: list[int] | None = None
    relations: list[dict] | None = None
    attachments: list[dict] | None = None
    pass

class GetPersonListDetails(PersonSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    icon: str | None = None
    created_time: datetime
    updated_time: datetime | None = None


class GetPersonDocListDetails(GetPersonListDetails):
    docs: list[dict]
    orgs: list[dict]
    persons: list[dict]
    attachments: list[dict] | None = None
    relations: list[dict] | None = None
    relation_json: dict | None = None
    activity: list[dict] | None
