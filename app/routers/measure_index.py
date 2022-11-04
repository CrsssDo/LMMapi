from fastapi import APIRouter, Depends, Response, status
from typing import List, Optional
from app.schemas.measure_index import MeasureIndexCreateRequest, MeasureIndexResponse, MeasureIndexUpdateStatusRequest
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.measure_index import MeasureIndexesService


router = APIRouter(
    prefix='/measure-indexes',
    tags=['Measure indexes']
)


@router.post('/', response_model=MeasureIndexResponse)
def create_measure_index(
    measure_data: MeasureIndexCreateRequest,
    current_user=Depends(get_authenticated_user),
    MeasureIndexesService: MeasureIndexesService = Depends(get_service(MeasureIndexesService))
):
    new_measure_index = MeasureIndexesService.create(measure_data)

    return new_measure_index


@router.get('/', response_model=List[MeasureIndexResponse])
def get_all_measure_indexes(
    measure_status: Optional[bool] = False,
    current_user=Depends(get_authenticated_user),
    MeasureIndexesService: MeasureIndexesService = Depends(get_service(MeasureIndexesService))
):
    measure_indexes = MeasureIndexesService.get_all(measure_status)

    return measure_indexes

@router.patch('/{id}', response_model=MeasureIndexResponse)
def update_measure_index(
    id: int,
    measure_data: MeasureIndexCreateRequest,
    current_user=Depends(get_authenticated_user),
    MeasureIndexesService: MeasureIndexesService = Depends(get_service(MeasureIndexesService))
):
    unit_update = MeasureIndexesService.update_measure_index(id, measure_data)

    return unit_update


@router.patch('/{id}/status', response_model=MeasureIndexResponse)
def update_measure_index_status(
    id: int,
    status: MeasureIndexUpdateStatusRequest,
    current_user=Depends(get_authenticated_user),
    MeasureIndexesService: MeasureIndexesService = Depends(get_service(MeasureIndexesService))
):
    unit_update = MeasureIndexesService.update_status(id, status)

    return unit_update


@router.get('/{id}', response_model=MeasureIndexResponse)
def get_unit_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    MeasureIndexesService: MeasureIndexesService = Depends(get_service(MeasureIndexesService))
):
    measure_index = MeasureIndexesService.get_by_id(id)

    return measure_index


@router.delete('/{id}/soft-delete')
def soft_delete_measure_index(
    id: int,
    current_user=Depends(get_authenticated_user),
    MeasureIndexesService: MeasureIndexesService = Depends(get_service(MeasureIndexesService))
):
    MeasureIndexesService.soft_delete_measure_index(id)

    return Response(status_code=status.HTTP_200_OK)






