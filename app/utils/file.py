import secrets
from fastapi import HTTPException, status, UploadFile
from PIL import Image
from app.core.settings import settings
import uuid
import boto3



def image_file(images):
    filename = images.filename
    extension = filename.split(".")[1]

    if extension not in ["png", "jpg","jpeg","gif", "docx", "pdf"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không hỗ trợ file {extension}",
        )

    return extension



def upload_photo_s3(file: UploadFile):
    upload_fullname = file.filename
    ext = upload_fullname.split(".")[-1]

    if ext not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File is not support {ext} extension")

    s3 = boto3.resource('s3', endpoint_url=settings.s3_url,
                            aws_access_key_id=settings.s3_access_key_id,
                            aws_secret_access_key=settings.s3_secret_access_key)
    bucket = s3.Bucket(settings.s3_bucket)
    new_filename = uuid.uuid4().hex + "." + ext
    bucket.upload_fileobj(file.file, new_filename, ExtraArgs={"ACL": "public-read"})
    return new_filename


def delete_file_s3(filename):
    s3 = boto3.resource('s3', endpoint_url=settings.s3_url,
                            aws_access_key_id=settings.s3_access_key_id,
                            aws_secret_access_key=settings.s3_secret_access_key)
    object = s3.Object(settings.s3_bucket, filename)
    object.delete()



