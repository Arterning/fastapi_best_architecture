#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import BIGINT, Column, ForeignKey, Integer, Table

from backend.common.model import MappedBase

sys_org_person = Table(
    'sys_org_person',
    MappedBase.metadata,
    Column('id', BIGINT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('org_id', BIGINT, ForeignKey('sys_org.id', ondelete='CASCADE'), primary_key=True, comment='组织ID'),
    Column('person_id', BIGINT, ForeignKey('sys_person.id', ondelete='CASCADE'), primary_key=True, comment='人物ID'),
)
