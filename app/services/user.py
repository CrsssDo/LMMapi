from base64 import encode
from typing import Optional
from fastapi import Depends, File,HTTPException, UploadFile, status, BackgroundTasks
from sqlalchemy import null, or_
from app.core.service import BaseService
from app.models.user import User
from app.schemas.user import UserUpdatePasswordRequest, UserCreateForm, UserUpdateForm, UserUpdateByAdminForm, UserUpdatePasswordByAdminRequest, UserUpdateStatusRequest
from app.utils.password import hash, verify
from app.utils.email import send_email_background, send_change_password_background, send_email_lock_user
from app.services.image import ImagesService
from jose import JWTError, jwt
from app.core.auth import get_reset_password_token, get_access_token
from app.core.settings import settings
from app.utils.generate import generate_code
from app.models.user_images import UserImages
from app.schemas.token import TokenData
import re


class UserService(BaseService):
    listUserRole = {
            "Super Admin" : [('Administrator'),('Area Manager'),('Operator Manager'),('Operator'),('Technician Manager'),('Technician'),('Reporter')],
            "Administrator" : [('Area Manager'),('Operator Manager'),('Operator'),('Technician Manager'),('Technician'),('Reporter')],
            "Area Manager" : [('Operator Manager'),('Operator'),('Technician Manager'),('Technician'),('Reporter')],
            "Operator Manager" : [('Operator')],
            "Technician Manager" : [('Technician')]
        }

    def get_by_id(self, id:str):
        user = self.db.query(User).filter(User.id == id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id: {id} does not exist")
        return user

    def create(self, 
        current_user: str,
        backround_task: BackgroundTasks,
        user_data: UserCreateForm = Depends(),
    ):
        user_in_query = self.db.query(User)
        user_email = user_in_query.filter(User.email == user_data.email).first()
        if user_email:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'email': f"Email đã được sử dụng.",
                    'type': 'type_error.unique'
                }]
            )

        user_phone = user_in_query.filter(User.phone == user_data.phone).first()
        if user_phone:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'phone': f"Số điện thoại đã được sử dụng.",
                    'type': 'type_error.unique'
                }]
            )

        if not user_data.role in self.listUserRole[current_user.role]:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'authorization': f"Bạn không được phép tạo người dùng này.",
                    'type': 'type_error.invalid'
                }]
            )

        max_id = self.db.execute("""
                SELECT MAX(id) from users
        """).first()
        code = max_id.max + 1
        prefix = 'NNV-'
        if code < 10:
            code_generate = f'{prefix}{0}{0}{0}{code}'
        elif code >= 10 and code < 100:
            code_generate = f'{prefix}{0}{0}{code}'
        elif code >=100 and code < 1000:
            code_generate = f'{prefix}{0}{code}'
        else:
            code_generate = f'{prefix}{code}'

        avatar_image_url = ''
        before_identity_image_url = ''
        after_identity_image_url = ''
        if user_data.avatar_image:
            avatar_photo = ImagesService.upload_photo_s3(user_data.avatar_image)
            avatar_image_url = f'{settings.s3_endpoint}/{avatar_photo}'

        if user_data.before_identity_image:
            before_identity_photo = ImagesService.upload_photo_s3(user_data.before_identity_image)
            before_identity_image_url = f'{settings.s3_endpoint}/{before_identity_photo}'

        if user_data.after_identity_image:
            after_identity_photo = ImagesService.upload_photo_s3(user_data.after_identity_image)
            after_identity_image_url = f'{settings.s3_endpoint}/{after_identity_photo}'

        password_generate = str(generate_code())
        new_user = User(
            email=user_data.email.lower(),
            password=hash(password_generate),
            code=code_generate,
            full_name=user_data.full_name,
            address=user_data.address,
            avatar_image_url=avatar_image_url,
            before_identity_image_url=before_identity_image_url,
            after_identity_image_url=after_identity_image_url,
            phone=user_data.phone,
            address_level_1_id=user_data.address_level_1_id,
            adopt_area_id=user_data.adopt_area_id,
            role=user_data.role
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        send_email_background(backround_task, user_data.email, password_generate, user_data.full_name, False)
        
        return new_user


    def get_all(self, current_user: str, adopt_id: Optional[int] = None):
        users = self.db.query(User).where(User.role.in_(self.listUserRole[current_user.role]))
        if adopt_id:
            users = users.filter(or_(User.adopt_area_id == adopt_id, User.role == 'Administrator'))

        return users.order_by(User.code).all()

    def update_user(self, id:int, user_data: UserUpdateForm):
        user = self.get_by_id(id)
        user_update = self.db.query(User).filter(User.id == id)
        if user_data.avatar_image_url:
            if user.avatar_image_url:
                file_name = user.avatar_image_url.lstrip(settings.s3_endpoint)
                ImagesService.delete_file_s3(self, file_name)
            avatar_photo = ImagesService.upload_photo_s3(user_data.avatar_image_url)
            avatar_image_url = f'{settings.s3_endpoint}/{avatar_photo}'
            user_update.update(
                {
                 "avatar_image_url" : avatar_image_url
                },
                synchronize_session=False
            )
        else:
            user_update.update(
                {"address": user_data.address,
                 "address_level_1_id": user_data.address_level_1_id,
                 "full_name": user_data.full_name
                },
                synchronize_session=False
            )

        self.db.commit()

        return user

    def update_user_password(self, id: int, user_data: UserUpdatePasswordRequest):
        user = self.get_by_id(id)
        if not verify(user_data.old_password, user.password):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'old_password': f"Mật khẩu hiện tại không chính xác.",
                    'type': 'type_error.invalid'
                }]
            )
            
        if user_data.new_password != user_data.retype_password:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'password': f"Mật khẩu không trùng khớp.",
                    'type': 'type_error.invalid'
                }]
            )
        self.db.query(User).filter(User.id == id).update({"password": hash(user_data.new_password)}, synchronize_session=False)
        self.db.commit()

        return user

    def update_user_password_by_admin(self, id: int,backround_task: BackgroundTasks, user_data: UserUpdatePasswordByAdminRequest):
        user = self.get_by_id(id)     
        if user_data.new_password != user_data.retype_password:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'password': f"Mật khẩu không trùng khớp.",
                    'type': 'type_error.invalid'
                }]
            )
        self.db.query(User).filter(User.id == id).update({"password": hash(user_data.new_password)}, synchronize_session=False)
        self.db.commit()

        if user_data.send_email == True:
            send_email_background(backround_task, user.email, user_data.new_password, user.full_name, True)

        return user

    
    def update_user_by_admin(self, id:int, user_data: UserUpdateByAdminForm, current_user: str,):
        user = self.get_by_id(id)

        if not user_data.role in self.listUserRole[current_user.role]:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'authorization': f"Bạn không được phép tạo người dùng này.",
                    'type': 'type_error.invalid'
                }]
            )

        user_update = self.db.query(User).filter(User.id == id)
        if user_data.before_identity_image:
            if user.before_identity_image_url:
                file_name = user.before_identity_image_url.lstrip(settings.s3_endpoint)
                ImagesService.delete_file_s3(self, file_name)
            before_identity_photo = ImagesService.upload_photo_s3(user_data.before_identity_image)
            before_identity_image_url = f'{settings.s3_endpoint}/{before_identity_photo}'
            user_update.update(
                {
                 "before_identity_image_url" : before_identity_image_url
                },
                synchronize_session=False
            )

        if user_data.after_identity_image:
            if user.after_identity_image_url:
                file_name = user.after_identity_image_url.lstrip(settings.s3_endpoint)
                ImagesService.delete_file_s3(self, file_name)
            after_identity_photo = ImagesService.upload_photo_s3(user_data.after_identity_image)
            after_identity_image_url = f'{settings.s3_endpoint}/{after_identity_photo}'
            user_update.update(
                {
                 "after_identity_image_url" : after_identity_image_url
                },
                synchronize_session=False
            )
        if user_data.full_name:
            user_update.update({"full_name": user_data.full_name },synchronize_session=False)

        if user_data.phone:
            user_update.update({"phone": user_data.phone },synchronize_session=False)

        if user_data.role:
            user_update.update({"role": user_data.role },synchronize_session=False)

        if user_data.address_level_1_id:
            user_update.update({"address_level_1_id": user_data.address_level_1_id },synchronize_session=False)

        self.db.commit()

        return user


    def upload_user_image(self, user_id:int, image_data: UploadFile = File(...)):
        self.get_by_id(user_id)

        filename = ImagesService.upload_photo_s3(image_data)
        image_url = f'{settings.s3_endpoint}/{filename}'

        user_other_image = UserImages(
                        user_id=user_id,
                        other_image_url=image_url
                    )
        self.db.add(user_other_image)

        self.db.commit()


    def delete_user_image(self, user_image_id:int):
        user_query = self.db.query(UserImages).filter(UserImages.id == user_image_id)

        user_image = user_query.first()

        if not user_image:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Hình ảnh không tồn tại"
            )

        file_name = user_image.other_image_url.lstrip(settings.s3_endpoint)
        ImagesService.delete_file_s3(self, file_name)

        user_query.delete(synchronize_session=False)
        self.db.commit()
                

    def delete_user(self, id:int):
        user = self.get_by_id(id)
        user_images = self.db.query(UserImages) \
            .filter(UserImages.user_id == id).all()
        if user_images:
            for img in user_images:
                file_name = img.other_image_url.lstrip(settings.s3_endpoint)
                ImagesService.delete_file_s3(self, file_name)
                
        if user.avatar_image_url:
            avatar_file_name = user.avatar_image_url.lstrip(settings.s3_endpoint)
            ImagesService.delete_file_s3(self, avatar_file_name)

        if user.before_identity_image_url:
            before_identity_file_name = user.before_identity_image_url.lstrip(settings.s3_endpoint)
            ImagesService.delete_file_s3(self, before_identity_file_name)

        if user.after_identity_image_url:
            after_identity_file_name = user.after_identity_image_url.lstrip(settings.s3_endpoint)
            ImagesService.delete_file_s3(self, after_identity_file_name)

        self.db.query(User).filter(User.id == id).delete(synchronize_session=False)

        self.db.commit()


    def get_request_change_password(self, user_infor: str, backround_task: BackgroundTasks, app: str):
        if user_infor.isnumeric():
            if not re.match(r"^(?=.*\d)(?=.*[0-9]).{10,10}$", user_infor):
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    [{
                        'validate': f"Sai số điện thoại.",
                        'type': 'type_error.invalid'
                    }]
                )
        else:
            if not re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", user_infor):
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    [{
                        'validate': f"Email không hợp lệ.",
                        'type': 'type_error.invalid'
                    }]
                )

        user_infor = user_infor.lower()
        user = self.db.query(User).filter(or_(User.email == user_infor, User.phone == user_infor)).first()

        if user:
            token = get_reset_password_token({"user_id": user.id})
            send_change_password_background(backround_task, user.email, user.full_name, token, app)

    def user_change_password(self, reset_token: str , new_password: str, confirm_password: str):
        payload = jwt.decode(reset_token, settings.secret_key, algorithms=[settings.algorithm])
        id: str = payload.get("user_id")
        token_data = TokenData(id=id)
      

        user = self.db.query(User).filter(User.id == token_data.id)

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise HTTPException(
                        status.HTTP_403_FORBIDDEN,
                        [{
                            'password': f"Mật khẩu không trùng khớp.",
                            'type': 'type_error.invalid'
                        }]
                    )

            user.update({"password": hash(new_password)}, synchronize_session=False)
            self.db.commit()

        user = user.first()

        token = get_access_token({"user_id": user.id})
    
        return {"access_token": token, "token_type": "bearer"}


    def update_user_status(self, id: int, backround_task: BackgroundTasks, user_update_data: UserUpdateStatusRequest):
        user = self.get_by_id(id)
        user_query = self.db.query(User).filter(User.id == id)
       
        user_query.update({"active": user_update_data.active}, synchronize_session=False)

        if user_update_data.unactivated_reason:
            user_query.update({"unactivated_reason": user_update_data.unactivated_reason}, synchronize_session=False)

        self.db.commit()

        send_email_lock_user(backround_task, user.email, user.full_name, user_update_data.unactivated_reason, user_update_data.active)

        return user

        
