#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import BIGINT, Column, ForeignKey, Integer, Table

from backend.common.model import MappedBase

# 外键的字段类型必须和主表的主键类型一致 

sys_sub_org = Table(
    'sys_sub_org',
    MappedBase.metadata,
    Column('id', BIGINT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('org_id', BIGINT, ForeignKey('sys_org.id', ondelete='CASCADE'), primary_key=True, comment='组织ID'),
    Column('subject_id', BIGINT, ForeignKey('sys_subject.id', ondelete='CASCADE'), primary_key=True, comment='议题ID'),
)
