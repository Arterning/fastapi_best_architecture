#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
from backend.common.model import Base, id_key


class PersonRelation(Base):
    __tablename__ = 'sys_person_relation'
    id: Mapped[id_key] = mapped_column(BigInteger, init=False)
    person_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_person.id', ondelete='SET NULL'), default=None, index=True, comment='人物ID'
    )
    other_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_person.id', ondelete='SET NULL'), default=None, index=True, comment='人物ID'
    )
    detail: Mapped[str | None] = mapped_column(String(255), default=None, comment='关系详情')