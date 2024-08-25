from fastapi import APIRouter, File, UploadFile
from backend.core.conf import settings
from backend.common.response.response_schema import response_base
from backend.app.admin.service.doc_service import doc_service
from typing import Tuple
from backend.utils.oss_client import minio_client
from backend.utils.ocr import extract_content_fitz

import asyncio

bucket_name = settings.BUCKET_NAME


router = APIRouter()

@router.get("/ocr_doc/{id}", summary='ocr转换')
async def ocr_doc(id: str):
    doc = await doc_service.get(pk=id)
    uid = doc.uuid
    file_name = f"{uid}.pdf"
    response = minio_client.get_object(bucket_name, file_name)
    file_content = response.read()
    loop = asyncio.get_event_loop()
    ocr_res, content = await loop.run_in_executor(None, extract_content_fitz, file_content)
    data = {
        "ocr_res": ocr_res,
        "content": content
    }
    await doc_service.base_update(pk=id, obj=data)
    return await response_base.success(data=data)
