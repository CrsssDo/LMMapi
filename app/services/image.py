from typing import Optional
from app.core.service import BaseService
from fastapi import HTTPException, status, Response, UploadFile, File
import boto3
from app.core.settings import settings
import uuid

from app.models.image import Images


class ImagesService(BaseService):

    def upload_photo_s3(file: UploadFile):
        upload_fullname = file.filename
        ext = upload_fullname.split(".")[-1]

        if ext not in ["png", "jpg", "jpeg", "gif", "docx", "pdf"]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Không hỗ trợ file {ext}")

        s3 = boto3.resource('s3', endpoint_url=settings.s3_url,
                            aws_access_key_id=settings.s3_access_key_id,
                            aws_secret_access_key=settings.s3_secret_access_key)
        bucket = s3.Bucket(settings.s3_bucket)
        new_filename = uuid.uuid4().hex + "." + ext
        bucket.upload_fileobj(file.file, new_filename, ExtraArgs={"ACL": "public-read"})
        return new_filename

    def delete_file_s3(self, filename):
        s3 = boto3.resource('s3', endpoint_url=settings.s3_url,
                            aws_access_key_id=settings.s3_access_key_id,
                            aws_secret_access_key=settings.s3_secret_access_key)
        object = s3.Object(settings.s3_bucket, filename)
        object.delete()

    def upload_image(self, record_id: int, record_type: str, ext: str, file_name: str, url: str, sub_type: Optional[str] = None):

        new_image = Images(
            record_id=record_id,
            record_type=record_type,
            ext=ext,
            file_name=file_name,
            url=url,
            sub_type=sub_type
        )
        self.db.add(new_image)
        self.db.flush()


    def delete_image(self, id: int):
        image_query = self.db.query(Images).filter(Images.id == id)
        image = image_query.first()

        if not image:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Hình ảnh không tồn tại"
            )

        self.delete_file_s3(image.file_name)

        image_query.delete(synchronize_session=False)
        self.db.commit()




