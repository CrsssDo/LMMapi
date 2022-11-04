from fastapi import APIRouter, Depends, Response, status, UploadFile, File, Body
from typing import List
from app.schemas.fish_type import FishTypesResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.fish_type import FishTypesService


router = APIRouter(
    prefix='/fish-types',
    tags=['Fish types']
)


@router.post('/', response_model=FishTypesResponse)
def create_fish_type(
    name: str = Body(...),
    current_user=Depends(get_authenticated_user),
    FishTypesService: FishTypesService = Depends(get_service(FishTypesService))
):
    new_fish_type = FishTypesService.create(name)

    return new_fish_type


@router.get('/', response_model=List[FishTypesResponse])
def get_all_fish_type(
    current_user=Depends(get_authenticated_user),
    FishTypesService: FishTypesService = Depends(get_service(FishTypesService))
):
    fish_type = FishTypesService.get_all()

    return fish_type

@router.patch('/{id}', response_model=FishTypesResponse)
def update_fish_type(
    id: int,
    name: str = Body(...),
    current_user=Depends(get_authenticated_user),
    FishTypesService: FishTypesService = Depends(get_service(FishTypesService))
):
    fish_type_update = FishTypesService.update_fish_type(id, name)

    return fish_type_update


@router.get('/{id}', response_model=FishTypesResponse)
def get_fish_type_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    FishTypesService: FishTypesService = Depends(get_service(FishTypesService))
):
    fish_type = FishTypesService.get_by_id(id)

    return fish_type


@router.delete('/{id}/soft-delete')
def soft_delete_fish_type(
    id: int,
    current_user=Depends(get_authenticated_user),
    FishTypesService: FishTypesService = Depends(get_service(FishTypesService))
):
    FishTypesService.soft_delete_fish_type(id)

    return Response(status_code=status.HTTP_200_OK)









