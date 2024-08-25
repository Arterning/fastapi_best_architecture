#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import BIGINT, Column, ForeignKey, Table

from backend.common.model import MappedBase

sys_doc_subject = Table(
    'sys_doc_subject',
    MappedBase.metadata,
    Column('id', BIGINT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('subject_id', BIGINT, ForeignKey('sys_subject.id', ondelete='CASCADE'), primary_key=True, comment='主题ID'),
    Column('doc_id', BIGINT, ForeignKey('sys_document.id', ondelete='CASCADE'), primary_key=True, comment='文档ID'),
)
