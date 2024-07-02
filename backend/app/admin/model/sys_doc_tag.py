#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import BIGINT, Column, ForeignKey, Table

from backend.common.model import MappedBase

sys_doc_tag = Table(
    'sys_doc_tag',
    MappedBase.metadata,
    Column('id', BIGINT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('tag_id', BIGINT, ForeignKey('sys_tag.id', ondelete='CASCADE'), primary_key=True, comment='标签ID'),
    Column('doc_id', BIGINT, ForeignKey('sys_document.id', ondelete='CASCADE'), primary_key=True, comment='文档ID'),
)
