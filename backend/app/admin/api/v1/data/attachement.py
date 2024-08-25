import uuid
import io
from minio.error import S3Error
from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from fastapi.responses import StreamingResponse
from backend.common.response.response_schema import response_base
from backend.utils.oss_client import minio_client
from backend.app.admin.schema.attachment import CreateAttachmentParam
from backend.app.admin.service.attachment_service import attachment_service

router = APIRouter()
bucket_name = "attachement"


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        uid = uuid.uuid4()
        obj_name = f"{uid}.{file.filename.split('.')[-1]}"

        # 上传文件到 MinIO
        file_content = await file.read()
        data = io.BytesIO(file_content)
        object_size = len(data.getbuffer())
        minio_client.put_object(bucket_name, obj_name, data, object_size, file.content_type)


        object_url = minio_client.presigned_get_object(bucket_name, obj_name)

        obj = CreateAttachmentParam(name=file.filename, uid=uid, obj_name=obj_name, url=object_url)
        attachment = await attachment_service.create(obj=obj)

        data =  {"id": attachment.id, "uid": uid, "obj_name": obj_name, "name": file.filename, "url": object_url}
        return await response_base.success(data=data)
    except S3Error as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.get("/preview/{obj_name}", summary = "获取图片")
async def preview(obj_name: str):
    try:
        response = minio_client.get_object(bucket_name, obj_name)
        
        async def file_generator(response):
            while True:
                chunk = response.read(9024)  # 逐块读取文件
                if not chunk:
                    break
                yield chunk
            response.close()
            response.release_conn()
        
        obj_type = obj_name.split('.')[-1]
        return StreamingResponse(file_generator(response), media_type=f'application/{obj_type}')
    except S3Error as err:
        raise HTTPException(status_code=404, detail="File not found")