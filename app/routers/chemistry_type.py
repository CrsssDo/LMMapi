from fastapi import APIRouter, Depends, Response, status, UploadFile, File, Body
from typing import List
from app.schemas.chemistry_type import ChemistryTypesResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.chemistry_type import ChemistryTypesService


router = APIRouter(
    prefix='/chemistry-types',
    tags=['Chemistry Types']
)


@router.post('/', response_model=ChemistryTypesResponse)
def create_chemistry_type(
    name: str = Body(...),
    current_user=Depends(get_authenticated_user),
    ChemistryTypesService: ChemistryTypesService = Depends(get_service(ChemistryTypesService))
):
    new_chemistry_type = ChemistryTypesService.create(name)

    return new_chemistry_type


@router.get('/', response_model=List[ChemistryTypesResponse])
def get_all_chemistry_type(
    current_user=Depends(get_authenticated_user),
    ChemistryTypesService: ChemistryTypesService = Depends(get_service(ChemistryTypesService))
):
    chemistry_type = ChemistryTypesService.get_all()

    return chemistry_type

@router.patch('/{id}', response_model=ChemistryTypesResponse)
def update_chemistry_type(
    id: int,
    name: str = Body(...),
    current_user=Depends(get_authenticated_user),
    ChemistryTypesService: ChemistryTypesService = Depends(get_service(ChemistryTypesService))
):
    chemistry_type_update = ChemistryTypesService.update_chemistry_type(id, name)

    return chemistry_type_update


@router.get('/{id}', response_model=ChemistryTypesResponse)
def get_chemistry_type_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    ChemistryTypesService: ChemistryTypesService = Depends(get_service(ChemistryTypesService))
):
    chemistry_type = ChemistryTypesService.get_by_id(id)

    return chemistry_type


@router.delete('/{id}/soft-delete')
def soft_delete_chemistry_type(
    id: int,
    current_user=Depends(get_authenticated_user),
    ChemistryTypesService: ChemistryTypesService = Depends(get_service(ChemistryTypesService))
):
    ChemistryTypesService.soft_delete_chemistry_type(id)

    return Response(status_code=status.HTTP_200_OK)









