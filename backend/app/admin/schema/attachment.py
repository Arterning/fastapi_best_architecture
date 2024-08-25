#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field
from backend.common.schema import SchemaBase
from uuid import UUID

class AttachmentSchemaBase(SchemaBase):
    name: str
    uid: UUID | None = None
    obj_name: str | None = None
    url: str | None = None
    person_id: int | None = None


class CreateAttachmentParam(AttachmentSchemaBase):
    pass


class UpdateAttachmentParam(AttachmentSchemaBase):
    pass


class GetAttachmentListDetails(AttachmentSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
