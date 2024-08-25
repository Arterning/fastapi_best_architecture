#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key


class Attachment(Base):
    __tablename__ = 'sys_attachment'

    id: Mapped[id_key] = mapped_column(BigInteger, init=False)
    uid: Mapped[str | None] = mapped_column(String(50), comment='uuid', default=None)
    obj_name: Mapped[str | None] = mapped_column(String(255), comment='对象存储名', default=None)
    name: Mapped[str | None] = mapped_column(String(255), comment='文件名', default=None)
    url: Mapped[str | None] = mapped_column(String(255), comment='url', default=None)

    person_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_person.id', ondelete='SET NULL'), default=None, index=True, comment='人物ID'
    )
    person: Mapped[Union['Person', None]] = relationship(init=False, back_populates='attachments')