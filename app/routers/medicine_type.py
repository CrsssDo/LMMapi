from fastapi import APIRouter, Depends, Response, status, UploadFile, File, Body
from typing import List
from app.schemas.medicine_type import MedicineTypesResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.medicine_type import MedicineTypesService


router = APIRouter(
    prefix='/medicine-types',
    tags=['Medicine Types']
)


@router.post('/', response_model=MedicineTypesResponse)
def create_medicine_type(
    name: str = Body(...),
    current_user=Depends(get_authenticated_user),
    MedicineTypesService: MedicineTypesService = Depends(get_service(MedicineTypesService))
):
    new_medicine_type = MedicineTypesService.create(name)

    return new_medicine_type


@router.get('/', response_model=List[MedicineTypesResponse])
def get_all_medicine_type(
    current_user=Depends(get_authenticated_user),
    MedicineTypesService: MedicineTypesService = Depends(get_service(MedicineTypesService))
):
    medicine_type = MedicineTypesService.get_all()

    return medicine_type

@router.patch('/{id}', response_model=MedicineTypesResponse)
def update_medicine_type(
    id: int,
    name: str = Body(...),
    current_user=Depends(get_authenticated_user),
    MedicineTypesService: MedicineTypesService = Depends(get_service(MedicineTypesService))
):
    medicine_type_update = MedicineTypesService.update_medicine_type(id, name)

    return medicine_type_update


@router.get('/{id}', response_model=MedicineTypesResponse)
def get_medicine_type_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    MedicineTypesService: MedicineTypesService = Depends(get_service(MedicineTypesService))
):
    medicine_type = MedicineTypesService.get_by_id(id)

    return medicine_type


@router.delete('/{id}/soft-delete')
def soft_delete_medicine_type(
    id: int,
    current_user=Depends(get_authenticated_user),
    MedicineTypesService: MedicineTypesService = Depends(get_service(MedicineTypesService))
):
    MedicineTypesService.soft_delete_medicine_type(id)

    return Response(status_code=status.HTTP_200_OK)









