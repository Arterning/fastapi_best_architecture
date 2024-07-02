#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class TagSchemaBase(SchemaBase):
    name: str
    detail: str | None = None


class CreateTagParam(TagSchemaBase):
    pass

class UpdateTagParam(TagSchemaBase):
    pass

class GetTagListDetails(TagSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None