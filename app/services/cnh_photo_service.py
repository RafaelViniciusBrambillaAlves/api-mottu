import uuid
from fastapi import UploadFile, status
from minio.error import S3Error 

from app.core.minio import get_minio_client
from app.core.config import settings
from app.core.exceptions import AppException

class CNHPhotoService:

    @staticmethod
    def upload(user_id: int, file: UploadFile) -> str:
        if file.content_type not in ("image/bmp", "image/png"):
            raise AppException(
                error = "INVALID_IMAGE_FORMAT", 
                message = "Invalid image format. Only PNG and BMP are allowed.",
                status_code = status.HTTP_406_NOT_ACCEPTABLE
            )
        
        client = get_minio_client()
        object_name = f"cnh/{user_id}/{uuid.uuid4()}-{file.filename}"

        try:
            client.put_object(
                bucket_name = settings.MINIO_BUCKET,
                object_name = object_name,
                data = file.file,
                length = -1,
                part_size = 10 * 1024 * 1024,
                content_type = file.content_type
            )
        except S3Error as e:
            raise AppException(
                error = "MINIO_UPLOAD_ERROR",
                message = "Error uploading CNH photoo", 
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e    
        
        return object_name