#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field
from uuid import UUID
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase

from backend.app.admin.schema.tag import GetTagListDetails

class DocSchemaBase(SchemaBase):
    title: str
    content: str
    subject: str | None  = None
    url: str | None = None
    uuid: UUID | None = None


class CreateDocParam(DocSchemaBase):
    tags: list[str] | None = None
    pass

class UpdateDocParam(DocSchemaBase):
    tags: list[str] | None = None
    pass

class GetDocList(DocSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None



class GetDocListDetails(DocSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tags: list[GetTagListDetails]
    created_time: datetime
    updated_time: datetime | None = None