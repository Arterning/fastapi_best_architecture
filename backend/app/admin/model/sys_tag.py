#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger

from backend.common.model import Base, id_key
from backend.app.admin.model.sys_doc_tag import sys_doc_tag


class Tag(Base):
    """系统api"""

    __tablename__ = 'sys_tag'

    id: Mapped[id_key] = mapped_column(BigInteger, init=False)
    name: Mapped[str] = mapped_column(String(50), comment='tag名称')
    detail: Mapped[str| None] = mapped_column(LONGTEXT, comment='tag详情')

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_user.id', ondelete='SET NULL'), default=None, comment='用户关联ID'
    )
    user: Mapped[Union['User', None]] = relationship(init=False, back_populates='tags')

    docs: Mapped[list['Document']] = relationship(
        init=False, secondary=sys_doc_tag, back_populates='tags'
    )

