from fastapi import APIRouter, Depends, Response, status
from typing import List
from app.schemas.pond import PondTypesResponse, PondTypeCreateRquest
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.pond import PondTypesService


router = APIRouter(
    prefix='/pond-type',
    tags=['Pond type']
)

@router.post('/')
def create_pond_type(
    pond_type_data: PondTypeCreateRquest,
    current_user=Depends(get_authenticated_user),
    PondTypesService: PondTypesService = Depends(get_service(PondTypesService))
):
    new_pond_type = PondTypesService.create(pond_type_data)

    return new_pond_type

@router.get('/', response_model=List[PondTypesResponse])
def get_all_pond_types(
    current_user=Depends(get_authenticated_user),
    PondTypesService: PondTypesService = Depends(get_service(PondTypesService))
):
    pond_types = PondTypesService.get_all()

    return pond_types

@router.get('/{id}', response_model=PondTypesResponse)
def get_pond_type_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    PondTypesService: PondTypesService = Depends(get_service(PondTypesService))
):
    pond_type = PondTypesService.get_by_id(id)

    return pond_type


@router.patch('/{id}', response_model=PondTypesResponse)
def update_pond_type(
    id: int,
    pond_type_data: PondTypeCreateRquest,
    current_user=Depends(get_authenticated_user),
    PondTypesService: PondTypesService = Depends(get_service(PondTypesService))
):
    pond_type_update = PondTypesService.update_pond_type(id, pond_type_data)

    return pond_type_update


@router.delete('/{id}/soft-delete')
def soft_delete_pond_type(
    id: int,
    current_user=Depends(get_authenticated_user),
    PondTypesService: PondTypesService = Depends(get_service(PondTypesService))
):
    PondTypesService.soft_delete_pond_type(id)

    return Response(status_code=status.HTTP_200_OK)
