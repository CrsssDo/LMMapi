from fastapi import APIRouter, Depends, Response, status
from typing import List
from app.schemas.adopt import AdoptResponse, AdoptUpdateRequest, AdoptCreateRequest
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.adopt import AdoptsService


router = APIRouter(
    prefix='/adopts',
    tags=['Adopts']
)


@router.post('/', response_model=AdoptResponse)
def create_adopt(
    adopt_data: AdoptCreateRequest,
    current_user=Depends(get_authenticated_user),
    AdoptsService: AdoptsService = Depends(get_service(AdoptsService))
):
    new_adopt = AdoptsService.create(adopt_data)

    return new_adopt


@router.get('/', response_model=List[AdoptResponse])
def get_all_adopts(
    current_user=Depends(get_authenticated_user),
    AdoptsService: AdoptsService = Depends(get_service(AdoptsService))
):
    adopts = AdoptsService.get_all()

    return adopts

@router.patch('/{id}', response_model=AdoptResponse)
def update_adopt(
    id: int,
    adopt_data: AdoptUpdateRequest,
    current_user=Depends(get_authenticated_user),
    AdoptsService: AdoptsService = Depends(get_service(AdoptsService))
):
    adopt_update = AdoptsService.update_adopt(id, adopt_data)

    return adopt_update


@router.get('/{id}', response_model=AdoptResponse)
def get_adopt_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    AdoptsService: AdoptsService = Depends(get_service(AdoptsService))
):
    adopt = AdoptsService.get_by_id(id)

    return adopt








