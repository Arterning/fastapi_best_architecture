#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import BIGINT, Column, ForeignKey, Integer, Table

from backend.common.model import MappedBase

sys_sub_person = Table(
    'sys_sub_person',
    MappedBase.metadata,
    Column('id', BIGINT, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    Column('person_id', BIGINT, ForeignKey('sys_person.id', ondelete='CASCADE'), primary_key=True, comment='人物ID'),
    Column('subject_id', BIGINT, ForeignKey('sys_subject.id', ondelete='CASCADE'), primary_key=True, comment='议题ID'),
)
