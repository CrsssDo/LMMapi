from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Body, Depends, File,Response, UploadFile, status, HTTPException
from app.core.auth import get_authenticated_user
from app.schemas.user import UserResponse, UserUpdatePasswordRequest, UserCreateForm, UserUpdateForm, UserUpdateByAdminForm, UserUpdatePasswordByAdminRequest, UserUpdateStatusRequest
from app.services.user import UserService
from app.core.service import get_service


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/me', response_model=UserResponse)
def get_me(current_user=Depends(get_authenticated_user)):
    return current_user


@router.post('/', response_model=UserResponse)
def create_user(
    background_task: BackgroundTasks,
    user_request: UserCreateForm = Depends(),
    current_user=Depends(get_authenticated_user),
    UserService: UserService = Depends(get_service(UserService))
):
    new_user = UserService.create(current_user, background_task, user_request)

    return new_user


@router.get('/', response_model=List[UserResponse])
def get_all_user(
    adopt_id: Optional[int] = None,
    current_user=Depends(get_authenticated_user),
    UserService: UserService = Depends(get_service(UserService))
):
    users = UserService.get_all(current_user, adopt_id)

    return users


@router.patch('/change-password')
def user_change_password(
    new_password: str = Body(...),
    confirm_password: str = Body(...),
    reset_token: str = Body(...),
    UserService: UserService = Depends(get_service(UserService))
):
    user = UserService.user_change_password(reset_token, new_password, confirm_password)

    return user


@router.patch('/{id}', response_model=UserResponse)
def update_user(
    id: int,
    user_data: UserUpdateForm = Depends(),
    current_user=Depends(get_authenticated_user),
    UserService: UserService = Depends(get_service(UserService))
):
    user_update = UserService.update_user(id, user_data)

    return user_update


@router.patch('/{id}/admin', response_model=UserResponse)
def update_user_by_admin(
    id: int,
    user_data: UserUpdateByAdminForm = Depends(),
    current_user=Depends(get_authenticated_user),
    UserService: UserService = Depends(get_service(UserService))
):
    user_update = UserService.update_user_by_admin(id, user_data, current_user)

    return user_update


@router.patch('/{id}/password', response_model=UserResponse)
def update_user_password(
    id: int,
    user_data: UserUpdatePasswordRequest,
    current_user=Depends(get_authenticated_user),
    UserService: UserService = Depends(get_service(UserService))
):
    user_update = UserService.update_user_password(id, user_data)

    return user_update


@router.patch('/{id}/password-admin', response_model=UserResponse)
def update_password_by_admin(
    id: int,
    backround_task: BackgroundTasks,
    user_data: UserUpdatePasswordByAdminRequest,
    current_user=Depends(get_authenticated_user),
    UserService: UserService = Depends(get_service(UserService))
):
    user_update = UserService.update_user_password_by_admin(id, backround_task, user_data)

    return user_update


@router.get('/forget-password', response_model=UserResponse)
def get_request_change_password_for_user(
    backround_task: BackgroundTasks,
    email: str,
    app: str,
    UserService: UserService = Depends(get_service(UserService))
):
    UserService.get_request_change_password(email, backround_task, app)



@router.delete('/{id}')
def delete_user(
    id: int,
    current_user=Depends(get_authenticated_user),
    UserService: UserService = Depends(get_service(UserService))
):
    UserService.delete_user(id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/{id}', response_model=UserResponse)
def get_user_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    UserService: UserService = Depends(get_service(UserService))
):
    user = UserService.get_by_id(id)

    return user


@router.post("/{user_id}/image")
def upload_user_image(
        user_id: int,
        image_data: UploadFile = File(...),
        current_user=Depends(get_authenticated_user),
        UserService: UserService = Depends(get_service(UserService))
):
    UserService.upload_user_image(user_id, image_data)

    return Response(status_code=status.HTTP_200_OK)



@router.delete("/{user_image_id}/image")
def delete_user_image(
        user_image_id: int,
        current_user=Depends(get_authenticated_user),
        UserService: UserService = Depends(get_service(UserService))
):
    UserService.delete_user_image(user_image_id)

    return Response(status_code=status.HTTP_200_OK)


@router.patch('/{id}/status', response_model=UserResponse)
def user_update_status(
    id: int,
    backround_task: BackgroundTasks,
    user_update_data: UserUpdateStatusRequest,
    UserService: UserService = Depends(get_service(UserService))
):
    user = UserService.update_user_status(id, backround_task, user_update_data)

    return user
