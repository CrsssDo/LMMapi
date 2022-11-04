from datetime import datetime, timedelta
from re import T
from fastapi import APIRouter, Depends
from typing import List
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.medicine_in import MedicineInsService
from app.schemas.medicine_in import MedicineInResponse, MedicineInCreate, MedicineInFilter, MedicineInUpdateRequest


router = APIRouter(
    prefix='/medicine-in',
    tags=['Medicine in']
)


@router.post('/', response_model=MedicineInResponse)
def create_medicine_in(
    medicine_data: MedicineInCreate,
    current_user=Depends(get_authenticated_user),
    MedicineInsService: MedicineInsService = Depends(get_service(MedicineInsService))
):
    new_medicine = MedicineInsService.create(medicine_data)

    return new_medicine


@router.get('/', response_model=List[MedicineInResponse])
def get_all_medicine_in_by_medicine_id(
    medicine_in_filter: MedicineInFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    MedicineInsService: MedicineInsService = Depends(get_service(MedicineInsService))
):
    medicine_ins = MedicineInsService.get_all(medicine_in_filter, all=True)

    return medicine_ins


@router.get('/{id}', response_model=MedicineInResponse)
def get_medicine_in_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    MedicineInsService: MedicineInsService = Depends(get_service(MedicineInsService))
):
    medicine_in = MedicineInsService.get_by_id(id)

    return medicine_in


@router.post('/excel-report/', response_model=List[MedicineInResponse])
def export_medicine_in_report(
    medicine_in_filter: MedicineInFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    MedicineInsService: MedicineInsService = Depends(get_service(MedicineInsService))
):
    if medicine_in_filter.from_date is None and medicine_in_filter.to_date is None:
        medicine_in_filter.to_date = datetime.now()
        medicine_in_filter.from_date  = medicine_in_filter.to_date - timedelta(days=30)

    medicine_in_reports = MedicineInsService.get_all(medicine_in_filter, all=False)

    return medicine_in_reports


@router.patch('/{id}', response_model=MedicineInResponse)
def update_medicine_in_by_id(
    id: int,
    medicine_in_update_data: MedicineInUpdateRequest,
    current_user=Depends(get_authenticated_user),
    MedicineInsService: MedicineInsService = Depends(get_service(MedicineInsService))
):
    medicine_in = MedicineInsService.update(id, medicine_in_update_data)

    return medicine_in




