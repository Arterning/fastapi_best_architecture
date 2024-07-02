#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import INT, BIGINT, Column, ForeignKey, Table

from backend.common.model import MappedBase

sys_user_doc = Table(
    'sys_user_doc',
    MappedBase.metadata,
    Column('id', INT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('user_id', INT, ForeignKey('sys_user.id', ondelete='CASCADE'), primary_key=True, comment='用户ID'),
    Column('doc_id', BIGINT, ForeignKey('sys_document.id', ondelete='CASCADE'), primary_key=True, comment='文档ID'),
)
