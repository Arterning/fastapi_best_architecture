#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import Annotated
import time

from fastapi import APIRouter, Depends, Path, Query, BackgroundTasks, FastAPI
from fastapi.responses import FileResponse

from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db_mysql import CurrentSession

from backend.utils.serializers import select_as_dict
from backend.app.admin.service.doc_service import doc_service
from backend.app.admin.schema.doc import CreateDocParam, UpdateDocParam, GetDocListDetails, GetDocList
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from fastapi import FastAPI, File, UploadFile, Response, Request

from minio import Minio
from minio.error import S3Error
import zipfile
import fitz
import io
import os
import uuid

import traceback
from datetime import datetime
from backend.common.log import log
from backend.core.conf import settings


router = APIRouter()

bucket_name = settings.BUCKET_NAME
minio_client = Minio(
    settings.MINIO_URL,
    access_key=settings.ACCESS_KEY,
    secret_key=settings.SECRET_KEY,
    secure=False  # Change to True if Minio is using HTTPS
)

temp_path = settings.TEMP_PATH


@router.get(
    '',
    summary='（模糊条件）分页获取所有接口',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_docs(
    db: CurrentSession,
    request: Request,
    title: Annotated[list[str] | None, Query()] = [],
    rangeValue: Annotated[list[str] | None, Query()] = ['', ''],
    tags: Annotated[list[int] | None, Query()] = None,
    follow: Annotated[bool | None, Query()] = False,
) -> ResponseModel:
    ids = None
    if follow:
        user_id = request.user.id
        ids = await doc_service.get_follow_doc_ids(user_id)
    doc_select = await doc_service.get_select(ids=ids, title=title, rangeValue=rangeValue, tags=tags)
    page_data = await paging_data(db, doc_select, GetDocListDetails)
    return await response_base.success(data=page_data)

@router.get('/all', summary='获取所有文件', 
    dependencies=[
        DependsJwtAuth,
    ])
async def get_all_docs(title: Annotated[str | None, Query()] = None) -> ResponseModel:
    docs = await doc_service.get_all(title=title)
    data = [GetDocList(**await select_as_dict(doc)) for doc in docs]
    return await response_base.success(data=data)


@router.get(
    '/follow',
    summary='收藏接口',
    dependencies=[
        DependsJwtAuth,
    ],
)
async def follow_doc(request: Request, id: Annotated[int | None, Query()] = None) -> ResponseModel:
    user_id = request.user.id
    await doc_service.follow_doc(user_id=user_id, doc_id=id)
    return await response_base.success()


@router.get(
    '/unfollow',
    summary='取消收藏接口',
    dependencies=[
        DependsJwtAuth,
    ],
)
async def unfollow_doc(request: Request, id: Annotated[int | None, Query()] = None) -> ResponseModel:
    user_id = request.user.id
    await doc_service.unfollow_doc(user_id, id)
    return await response_base.success()


@router.get('/{pk}', summary='获取文件详情',
    dependencies=[
        DependsJwtAuth,
    ])
async def get_doc(pk: Annotated[int, Path(...)]) -> ResponseModel:
    doc = await doc_service.get(pk=pk)
    data = GetDocListDetails(**await select_as_dict(doc))
    return await response_base.success(data=data)

@router.put(
    '/{pk}',
    summary='更新文件接口',
    dependencies=[
        DependsJwtAuth,
    ],
)
async def update_doc(request: Request, pk: Annotated[int, Path(...)], obj: UpdateDocParam) -> ResponseModel:
    user_id = request.user.id
    count = await doc_service.update(pk=pk, obj=obj, user_id=user_id)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '',
    summary='（批量）删除接口',
    dependencies=[
        DependsJwtAuth,
    ],
)
async def delete_doc(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    docs = await doc_service.get_by_ids(pk=pk)
    for doc in docs:
        log.info(f"Remove Document pdf: {doc.uuid}.pdf")
        if doc.uuid is not None:
            minio_client.remove_object(bucket_name, f"{doc.uuid}.pdf")

    count = await doc_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.post(
    '',
    summary='创建接口',
    dependencies=[
        DependsJwtAuth,
    ],
)
async def create_doc(request: Request, obj: CreateDocParam) -> ResponseModel:
    user_id = request.user.id
    new_doc = await doc_service.create(obj=obj, user_id=user_id)
    return await response_base.success()


@router.post('/upload', summary='上传文件',
    dependencies=[
        DependsJwtAuth,
    ],
)
async def upload(request: Request, file: Annotated[UploadFile, File()], background_tasks: BackgroundTasks) -> ResponseModel:
    user_id = request.user.id
    # 检查文件是否为PDF格式
    if file.content_type == 'application/pdf':
        file_content = await file.read()
        # 使用fitz读取PDF内容
        try:
            pdf_document = fitz.open(stream=file_content, filetype="pdf")
            text = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                text += page.get_text()
            text = "\n".join(line for line in text.split("\n") if line.strip())
            uid = uuid.uuid4()
            object_url = f"http://{settings.MINIO_URL}/{settings.BUCKET_NAME}/{uid}.pdf"
            title = file.filename
            subject = title.replace(".pdf", "")
            doc_time = extract_date_from_text(title)
            obj = CreateDocParam(title=title, content=text, time=doc_time, url=object_url, subject=subject, source="文件上传", uuid=uid, tags=[])
            new_doc = await doc_service.create(obj=obj, user_id=user_id)
            pdf_document.close()

            # Save the file to Minio
            pdf_data = io.BytesIO(file_content)
            object_size = len(pdf_data.getbuffer())
            minio_client.put_object(bucket_name, f"{uid}.pdf", pdf_data, object_size, "application/pdf")

        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Error reading PDF: " + str(e))

    if file.content_type == 'application/x-zip-compressed':
        time_stamp = time.time()
        temp_file = temp_path + f"{time_stamp}.zip"
        with open(temp_file, "wb") as f:
            f.write(await file.read())
        
        # 异步上传 
        background_tasks.add_task(read_zip_file, user_id=user_id, temp_file=temp_file)
        # await read_zip_file(user_id)
    return await response_base.success(data='上传成功')

async def read_zip_file(user_id, temp_file):
    with zipfile.ZipFile(temp_file, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.lower().endswith('.pdf'):
                with zip_ref.open(file_name) as pdf_file:
                    try:
                        new_doc = await read_single_file(user_id, file_name, pdf_file)
                        log.info(f"Success read {file_name} from zip file")
                    except Exception as e:
                        log.error(f"Error read {file_name} from zip file:" + str(e))
                        traceback.print_exc()
    os.remove(temp_file)


async def read_single_file(user_id, file_name, pdf_file):
    uid = uuid.uuid4()
    pdf_data = io.BytesIO(pdf_file.read())
    object_url = f"http://{settings.MINIO_URL}/{settings.BUCKET_NAME}/{uid}.pdf"
    pdf_document = fitz.open("pdf", pdf_data)
    pdf_text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        pdf_text += page.get_text("text")
    pdf_text = "\n".join(line for line in pdf_text.split("\n") if line.strip())
    title = os.path.basename(file_name)
    subject = title.replace(".pdf", "")
    obj = CreateDocParam(title=title, content=pdf_text, url=object_url, subject=subject, uuid=uid, tags=[])
    new_doc = await doc_service.create(obj=obj, user_id=user_id)

    object_size = len(pdf_data.getbuffer())
    minio_client.put_object(bucket_name, f"{uid}.pdf", pdf_data, object_size, "application/pdf")
    return new_doc


# Define a function to extract date from text
def extract_date_from_text(text):
    # Regex to find the numeric pattern in the text
    match = re.search(r'(\d{6})', text)
    if match:
        date_str = match.group(1)
        year = '20' + date_str[:2]
        month = date_str[2:4]
        day = date_str[4:6]
        return f"{year}年{month}月{day}日"
    else:
        return None

@router.get("/preview/{uid}", summary = "预览文件")
async def preview_pdf(uid: str):
    try:
        file_name = f"{uid}.pdf"
        # 从 MinIO 获取对象
        response = minio_client.get_object(bucket_name, file_name)
        
        async def file_generator(response):
            while True:
                chunk = response.read(9024)  # 逐块读取文件
                if not chunk:
                    break
                yield chunk
            response.close()
            response.release_conn()
        
        return StreamingResponse(file_generator(response), media_type='application/pdf')
    except S3Error as e:
        raise HTTPException(status_code=404, detail="File not found")

@router.get("/download/{uid}", summary = "下载文件")
async def download_pdf(uid: str, response: Response):
    try:
        file_name = f"{uid}.pdf"
        # 从 MinIO 获取对象
        response = minio_client.get_object(bucket_name, file_name)
        
        async def file_generator(response):
            while True:
                chunk = response.read(9024)  # 逐块读取文件
                if not chunk:
                    break
                yield chunk
            response.close()
            response.release_conn()
        
        return StreamingResponse(file_generator(response), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={file_name}"})
    except S3Error as err:
        raise HTTPException(status_code=404, detail="File not found")
