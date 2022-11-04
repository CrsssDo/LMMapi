from typing import List, Optional
from app.schemas.adopt import AdoptResponse
from app.schemas.address import AddressLevel1Response
from app.schemas.user_images import UserImagesResponse
from fastapi import UploadFile, File, Form
from enum import Enum

from pydantic import BaseModel, Field, EmailStr


class UsersRole(str, Enum):
    super_admin = 'Super Admin'
    administrator = 'Administrator'
    area_manager = 'Area Manager'
    operator_manager = 'Operator Manager'
    operator = 'Operator'
    technician_manager = 'Technician Manager'
    technician = 'Technician'
    reporter = 'Reporter'


class UserBase(BaseModel):
    address_level_1_id: int = None
    adopt_area_id: int = None

    class Config:
        orm_mode = True
        use_enum_values = True


class UserCreateForm():
    def __init__(
        self,
        email: EmailStr = Form(...),
        address: str = Form(...),
        full_name: str = Form(..., max_length=50),
        phone: str = Form(..., min_length=10, max_length=10),
        role: UsersRole = Form(...),
        address_level_1_id: int = Form(...),
        adopt_area_id: int = Form(...),
        avatar_image: Optional[UploadFile] = File(None),
        before_identity_image: Optional[UploadFile] = File(None),
        after_identity_image: Optional[UploadFile]  = File(None)
    ):
        self.email = email
        self.address = address
        self.full_name = full_name
        self.phone = phone
        self.role = role
        self.address_level_1_id = address_level_1_id
        self.adopt_area_id = adopt_area_id
        self.avatar_image = avatar_image
        self.before_identity_image = before_identity_image
        self.after_identity_image = after_identity_image
    def dict(self):
        return self.__dict__  


class UserUpdateForm():
    def __init__(
        self,
        address: str = Form(...),
        address_level_1_id: int = Form(...),
        full_name: str = Form(..., max_length=50),
        avatar_image_url: Optional[UploadFile] = File(None)
    ):
        self.address = address
        self.address_level_1_id = address_level_1_id
        self.full_name = full_name
        self.avatar_image_url = avatar_image_url
    def dict(self):
        return self.__dict__  


class UserUpdateByAdminForm():
    def __init__(
        self,
        full_name: Optional[str] = Form(None),
        phone: str = Form(..., min_length=10, max_length=10),
        role: UsersRole = Form(...),
        address_level_1_id: Optional[int] = Form(None),
        before_identity_image: Optional[UploadFile] = File(None),
        after_identity_image: Optional[UploadFile]  = File(None)
    ):
        self.full_name = full_name
        self.phone = phone
        self.role = role
        self.address_level_1_id = address_level_1_id
        self.before_identity_image = before_identity_image
        self.after_identity_image = after_identity_image
    def dict(self):
        return self.__dict__


class UserUpdatePasswordRequest(BaseModel):
    old_password: str = Field(...)
    new_password: str = Field(..., regex="^(?=.*\d)(?=.*[a-z]).{6,20}$")
    retype_password: str = Field(..., regex="^(?=.*\d)(?=.*[a-z]).{6,20}$")

    class Config:
        orm_mode = True

class UserUpdateStatusRequest(BaseModel):
    active: bool = Field(...)
    unactivated_reason: str = Field(...)

    class Config:
        orm_mode = True


class UserUpdatePasswordByAdminRequest(BaseModel):
    new_password: str = Field(..., regex="^(?=.*\d)(?=.*[a-z]).{6,20}$")
    retype_password: str = Field(..., regex="^(?=.*\d)(?=.*[a-z]).{6,20}$")
    send_email: Optional[bool] = False

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    id: int
    email: EmailStr
    code: str
    address: str
    avatar_image_url: str = None
    before_identity_image_url: str = None
    after_identity_image_url: str = None
    full_name: str
    phone: str
    active: bool = None
    unactivated_reason: str = None
    adopt_area: AdoptResponse = None
    address_level_1: AddressLevel1Response = None
    role: str
    images: List[UserImagesResponse] = []

    class Config:
        orm_mode = True
    
