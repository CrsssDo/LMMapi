from fastapi import APIRouter, Depends, Response, status
from typing import List
from app.schemas.unit import UnitCreateRequest, UnitUpdateRequest, UnitResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.unit import UnitsService


router = APIRouter(
    prefix='/units',
    tags=['Units']
)


@router.post('/')
def create_unit(
    unit_data: UnitCreateRequest,
    current_user=Depends(get_authenticated_user),
    UnitsService: UnitsService = Depends(get_service(UnitsService))
):
    new_unit = UnitsService.create(unit_data)

    return new_unit


@router.get('/', response_model=List[UnitResponse])
def get_all_unit(
    current_user=Depends(get_authenticated_user),
    UnitsService: UnitsService = Depends(get_service(UnitsService))
):
    units = UnitsService.get_all()

    return units

@router.patch('/{id}', response_model=UnitResponse)
def update_unit(
    id: int,
    unit_data: UnitUpdateRequest,
    current_user=Depends(get_authenticated_user),
    UnitsService: UnitsService = Depends(get_service(UnitsService)),
):
    unit_update = UnitsService.update_unit(id, unit_data)

    return unit_update

@router.get('/{id}', response_model=UnitResponse)
def get_unit_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    UnitsService: UnitsService = Depends(get_service(UnitsService))
):
    unit = UnitsService.get_by_id(id)

    return unit


@router.delete('/{id}/soft-delete')
def soft_delete_unit(
    id: int,
    current_user=Depends(get_authenticated_user),
    UnitsService: UnitsService = Depends(get_service(UnitsService))
):
    UnitsService.soft_delete_unit(id)

    return Response(status_code=status.HTTP_200_OK)





