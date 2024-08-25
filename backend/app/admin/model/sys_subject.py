#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, JSON

from backend.common.model import Base, id_key
from backend.app.admin.model.sys_doc_subject import sys_doc_subject
from backend.app.admin.model.sys_sub_person import sys_sub_person
from backend.app.admin.model.sys_sub_org import sys_sub_org

class Subject(Base):
    """主题"""

    __tablename__ = 'sys_subject'

    id: Mapped[id_key] = mapped_column(BigInteger, init=False)
    name: Mapped[str] = mapped_column(String(255), unique=True, comment='议题名称')
    type:  Mapped[str| None] = mapped_column(String(50), comment='议题类型', default=None)
    his: Mapped[list[dict] | None] = mapped_column(JSON, comment='议题脉络', default=None)
    detail: Mapped[str| None] = mapped_column(LONGTEXT, comment='议题详情', default=None)

    docs: Mapped[list['Document']] = relationship(
        init=False, secondary=sys_doc_subject, back_populates='subjects'
    )

    persons: Mapped[list['Person']] = relationship(
        init=False, secondary=sys_sub_person, back_populates='subjects'
    )

    orgs: Mapped[list['Organization']] = relationship(
        init=False, secondary=sys_sub_org, back_populates='subjects'
    )