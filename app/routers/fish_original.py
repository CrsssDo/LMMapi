from fastapi import APIRouter, Depends, Response, status, UploadFile, File
from typing import List
from app.schemas.fish_original import OriginFishCreateRequest, OriginFishResponse, OriginalFishUpdateRequest, OriginFishDetailResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.fish_original import OriginalFishesService


router = APIRouter(
    prefix='/original-fish',
    tags=['Original fishes']
)


@router.post('/', response_model=OriginFishResponse)
def create_original_fish(
    fish_data: OriginFishCreateRequest,
    current_user=Depends(get_authenticated_user),
    OriginalFishesService: OriginalFishesService = Depends(get_service(OriginalFishesService))
):
    new_original_fish = OriginalFishesService.create(fish_data)

    return new_original_fish


@router.get('/', response_model=List[OriginFishResponse])
def get_all_original_fishes(
    current_user=Depends(get_authenticated_user),
    OriginalFishesService: OriginalFishesService = Depends(get_service(OriginalFishesService))
):
    original_fish = OriginalFishesService.get_all()

    return original_fish

@router.patch('/{id}', response_model=OriginFishResponse)
def update_original_fish(
    id: int,
    fish_data: OriginalFishUpdateRequest,
    current_user=Depends(get_authenticated_user),
    OriginalFishesService: OriginalFishesService = Depends(get_service(OriginalFishesService))
):
    original_fish_update = OriginalFishesService.update_original_fish(id, fish_data)

    return original_fish_update


@router.get('/{id}', response_model=OriginFishDetailResponse)
def get_fish_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    OriginalFishesService: OriginalFishesService = Depends(get_service(OriginalFishesService))
):
    original_fish = OriginalFishesService.get_by_id(id)

    return original_fish


@router.post("/{origin_fish_id}/image")
def upload_origin_fish_image(
        origin_fish_id: int,
        image_data: UploadFile = File(...),
        current_user=Depends(get_authenticated_user),
        OriginalFishesService: OriginalFishesService = Depends(get_service(OriginalFishesService))
):
    OriginalFishesService.upload_origin_fish_image(origin_fish_id , image_data)

    return Response(status_code=status.HTTP_200_OK)


@router.post("/{origin_fish_id}/images")
def upload_multi_origin_fish_image(
        origin_fish_id: int,
        image_datas: List[UploadFile] = File(...),
        current_user=Depends(get_authenticated_user),
        OriginalFishesService: OriginalFishesService = Depends(get_service(OriginalFishesService))
):
    OriginalFishesService.upload_multi_origin_fish_image(origin_fish_id, image_datas)

    return Response(status_code=status.HTTP_200_OK)


@router.delete('/{id}/soft-delete')
def soft_delete_original_fish(
    id: int,
    current_user=Depends(get_authenticated_user),
    OriginalFishesService: OriginalFishesService = Depends(get_service(OriginalFishesService))
):
    OriginalFishesService.soft_delete_original_fish(id)

    return Response(status_code=status.HTTP_200_OK)




