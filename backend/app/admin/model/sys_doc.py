#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, JSON
from backend.common.model import Base, id_key
from backend.app.admin.model.sys_doc_tag import sys_doc_tag
from backend.app.admin.model.sys_user_doc import sys_user_doc

from backend.app.admin.model.sys_doc_person import sys_doc_person
from backend.app.admin.model.sys_doc_org import sys_doc_org
from backend.app.admin.model.sys_doc_subject import sys_doc_subject

class Document(Base):
    """系统api"""

    __tablename__ = 'sys_document'

    id: Mapped[id_key] = mapped_column(BigInteger, init=False)
    title: Mapped[str] = mapped_column(String(255), comment='标题')
    content: Mapped[str] = mapped_column(LONGTEXT, comment='内容')
    subject: Mapped[str | None] = mapped_column(LONGTEXT, comment='主题', default=None)
    url: Mapped[str | None] = mapped_column(LONGTEXT, comment='url', default=None)
    uuid: Mapped[str | None] = mapped_column(String(50), comment='uuid', default=None)
    ocr_res: Mapped[list[str] | None] = mapped_column(JSON, comment='ocr结果', default=None)

    tags: Mapped[list['Tag']] = relationship(
        init=False, secondary=sys_doc_tag, back_populates='docs'
    )

    followers: Mapped[list['User']] = relationship(
        init=False, secondary=sys_user_doc, back_populates='follow_docs'
    )

    persons: Mapped[list['Person']] = relationship(
        init=False, secondary=sys_doc_person, back_populates='docs'
    )

    orgs: Mapped[list['Organization']] = relationship(
        init=False, secondary=sys_doc_org, back_populates='docs'
    )

    
    subjects: Mapped[list['Subject']] = relationship(
        init=False, secondary=sys_doc_subject, back_populates='docs'
    )

