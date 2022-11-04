from pydantic import BaseSettings
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import ConnectionConfig


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    s3_url: str
    s3_access_key_id: str
    s3_secret_access_key: str
    s3_default_region: str
    s3_bucket: str
    s3_version: str
    s3_endpoint: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str
    MAIL_TLS: bool
    MAIL_SSL: bool
    server: str
    app_server: str

    class Config:
        env_file = ".env"
    

def Conf():
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.mail_username,
        MAIL_PASSWORD=settings.mail_password,
        MAIL_FROM=settings.mail_from,
        MAIL_PORT=settings.mail_port,
        MAIL_SERVER=settings.mail_server,
        MAIL_FROM_NAME=settings.mail_from_name,
        MAIL_TLS=settings.MAIL_TLS,
        MAIL_SSL=settings.MAIL_SSL,
        TEMPLATE_FOLDER='app/templates/'
    )
    return conf



settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')