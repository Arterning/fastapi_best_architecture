#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, JSON
from backend.common.model import Base, id_key
from datetime import datetime
from backend.app.admin.model.sys_doc_org import sys_doc_org
from backend.app.admin.model.sys_org_person import sys_org_person
from backend.app.admin.model.sys_sub_org import sys_sub_org


class Organization(Base):
    """系统api"""

    __tablename__ = 'sys_org'

    id: Mapped[id_key] = mapped_column(BigInteger, init=False)
    name: Mapped[str] = mapped_column(String(255), comment='组织名称')
    detail: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='组织详情')

    sort: Mapped[int] = mapped_column(default=0, comment='排序')

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_org.id', ondelete='SET NULL'), default=None, index=True, comment='父组织ID'
    )

    parent: Mapped[Union['Organization', None]] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[list['Organization'] | None] = relationship(init=False, back_populates='parent')

    persons: Mapped[list['Person']] = relationship(  # noqa: F821
        init=False, secondary=sys_org_person, back_populates='orgs'
    )

    docs: Mapped[list['Document']] = relationship(  # noqa: F821
        init=False, secondary=sys_doc_org, back_populates='orgs'
    )


    default_show: Mapped[bool] = mapped_column(default=False, comment='是否默认展示(0否 1是)')

    activity: Mapped[list[dict] | None] = mapped_column(JSON, comment='组织活动', default=None)

    subjects: Mapped[list['Subject']] = relationship(
        init=False, secondary=sys_sub_org, back_populates='orgs'
    )
