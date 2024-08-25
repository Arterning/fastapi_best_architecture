#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.admin.api.v1.data.attachement import router as attachment_router
from backend.app.admin.api.v1.data.doc import router as doc_router
from backend.app.admin.api.v1.data.tag import router as tag_router
from backend.app.admin.api.v1.data.ocr import router as ocr_router
from backend.app.admin.api.v1.data.org import router as org_router
from backend.app.admin.api.v1.data.person import router as person_router
from backend.app.admin.api.v1.data.subject import router as subject_router

router = APIRouter(prefix='/data')

router.include_router(attachment_router, prefix='/attachement', tags=['附件上传'])
router.include_router(doc_router, prefix='/docs', tags=['文件管理'])
router.include_router(tag_router, prefix='/tags', tags=['标签管理'])
router.include_router(ocr_router, prefix='/ocr', tags=['OCR识别'])
router.include_router(org_router, prefix='/orgs', tags=['机构管理'])
router.include_router(person_router, prefix='/persons', tags=['人物管理'])
router.include_router(subject_router, prefix='/subjects', tags=['议题管理'])