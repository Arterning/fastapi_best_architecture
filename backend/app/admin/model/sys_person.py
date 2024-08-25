#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, JSON
from backend.common.model import Base, id_key
from datetime import datetime
from backend.app.admin.model.sys_doc_person import sys_doc_person
from backend.app.admin.model.sys_org_person import sys_org_person
from backend.app.admin.model.sys_sub_person import sys_sub_person

class Person(Base):
    """系统api"""

    __tablename__ = 'sys_person'

    id: Mapped[id_key] = mapped_column(BigInteger, init=False)
    name: Mapped[str] = mapped_column(String(255), comment='人物名')
    icon: Mapped[str | None] = mapped_column(String(255), default=None, comment='人物头像')
    birth_date: Mapped[datetime | None] = mapped_column(default=None, comment='出生时间')

    detail: Mapped[str| None] = mapped_column(LONGTEXT, default=None, comment='人物详情')

    orgs: Mapped[list['Organization']] = relationship(
        init=False, secondary=sys_org_person, back_populates='persons'
    )

    docs: Mapped[list['Document']] = relationship(
        init=False, secondary=sys_doc_person, back_populates='persons'
    )


    attachments: Mapped[list['Attachment']] = relationship(init=False, back_populates='person')

    activity: Mapped[list[dict] | None] = mapped_column(JSON, comment='人物活动', default=None)

    subjects: Mapped[list['Subject']] = relationship(
        init=False, secondary=sys_sub_person, back_populates='persons'
    )