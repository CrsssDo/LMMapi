from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from typing import List

from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.chemistry_in import ChemistryInService
from app.schemas.chemistry_in import ChemistryInResponse, ChemistryInFilter, ChemistryInCreateRequest, ChemistryInUpdateRequest


router = APIRouter(
    prefix='/chemistry-in',
    tags=['Chemistry in']
)


@router.post('/', response_model=ChemistryInResponse)
def create_chemistry_in(
    chemistry_in_data: ChemistryInCreateRequest,
    current_user=Depends(get_authenticated_user),
    ChemistryInService: ChemistryInService = Depends(get_service(ChemistryInService))
):
    new_chemistry = ChemistryInService.create(chemistry_in_data)

    return new_chemistry


@router.get('/', response_model=List[ChemistryInResponse])
def get_all_chemistry_in_by_food_id(
    chemistry_filter_data: ChemistryInFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    ChemistryInService: ChemistryInService = Depends(get_service(ChemistryInService))
):
    chemistry_ins = ChemistryInService.get_all(chemistry_filter_data, True)

    return chemistry_ins


@router.get('/{id}', response_model=ChemistryInResponse)
def get_chemistry_in_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    ChemistryInService: ChemistryInService = Depends(get_service(ChemistryInService))
):
    chemistry_in = ChemistryInService.get_by_id(id)

    return chemistry_in


@router.post('/excel-report/', response_model=List[ChemistryInResponse])
def export_food_in_report(
    chemistry_filter_data: ChemistryInFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    ChemistryInService: ChemistryInService = Depends(get_service(ChemistryInService))
):
    if chemistry_filter_data.from_date is None and chemistry_filter_data.to_date is None:
        chemistry_filter_data.to_date = datetime.now()
        chemistry_filter_data.from_date  = chemistry_filter_data.to_date - timedelta(days=30)

    chemistry_in_report = ChemistryInService.get_all(chemistry_filter_data, False)

    return chemistry_in_report


@router.patch('/{id}', response_model=ChemistryInResponse)
def update_chemistry_in_by_id(
    id: int,
    chemistry_in_update_data: ChemistryInUpdateRequest,
    current_user=Depends(get_authenticated_user),
    ChemistryInService: ChemistryInService = Depends(get_service(ChemistryInService))
):
    chemistry_in = ChemistryInService.update(id, chemistry_in_update_data)

    return chemistry_in

