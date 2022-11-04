from fastapi import APIRouter, Depends, Response, status, UploadFile, File
from typing import List
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.environment_renovation import EnvironemntRenovationsService
from app.schemas.environment_renovation import EnvironmentRenovationCreateRequest, EnvironmentRenovationResponse, EnvironmentRenovationHistoryResponse


router = APIRouter(
    prefix='/environment-renovations',
    tags=['Environment renovation']
)


@router.post('/', response_model=EnvironmentRenovationResponse)
def create_environment_renovations(
    renovation_data: EnvironmentRenovationCreateRequest,
    current_user=Depends(get_authenticated_user),
    EnvironemntRenovationsService: EnvironemntRenovationsService = Depends(get_service(EnvironemntRenovationsService))
):
    new_renovation = EnvironemntRenovationsService.create(renovation_data)

    return new_renovation


@router.get('/', response_model=List[EnvironmentRenovationResponse])
def get_all_environment_renovation(
    pond_id: int,
    current_user=Depends(get_authenticated_user),
    EnvironemntRenovationsService: EnvironemntRenovationsService = Depends(get_service(EnvironemntRenovationsService))
):
    renovations = EnvironemntRenovationsService.get_all(pond_id)

    return renovations

@router.get("/{id}", response_model=EnvironmentRenovationResponse)
def get_environment_renovation_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    EnvironemntRenovationsService: EnvironemntRenovationsService = Depends(get_service(EnvironemntRenovationsService))
):
    renovation = EnvironemntRenovationsService.get_by_id(id)

    return renovation

@router.patch('/{id}', response_model=EnvironmentRenovationResponse)
def update_environment_renovation(
    id: int,
    renovation_data: EnvironmentRenovationCreateRequest,
    current_user=Depends(get_authenticated_user),
    EnvironemntRenovationsService: EnvironemntRenovationsService = Depends(get_service(EnvironemntRenovationsService))
):
    update_renovation = EnvironemntRenovationsService.update(id, renovation_data)

    return update_renovation


@router.get('/{pond_id}/history', response_model=List[EnvironmentRenovationHistoryResponse])
def get_all_environment_renovation_history(
    pond_id: int,
    current_user=Depends(get_authenticated_user),
    EnvironemntRenovationsService: EnvironemntRenovationsService = Depends(get_service(EnvironemntRenovationsService))
):
    renovations = EnvironemntRenovationsService.get_environment_renovation_history(pond_id)

    return renovations