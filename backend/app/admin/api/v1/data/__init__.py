#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.admin.api.v1.data.doc import router as doc_router
from backend.app.admin.api.v1.data.tag import router as tag_router

router = APIRouter(prefix='/data')

router.include_router(doc_router, prefix='/docs', tags=['文件管理'])
router.include_router(tag_router, prefix='/tags', tags=['标签管理'])