from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from typing import List
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.medicine_out import MedicineOutsService
from app.schemas.medicine_out import MedicineOutResponse, MedicineOutCreate, MedicineOutFilter, MedicineOutHistoryValue, MedicineOutHistoryResponse


router = APIRouter(
    prefix='/medicine-out',
    tags=['Medicine out']
)


@router.post('/', response_model=MedicineOutResponse)
def create_medicine_out(
    medicine_data: MedicineOutCreate,
    current_user=Depends(get_authenticated_user),
    MedicineOutsService: MedicineOutsService = Depends(get_service(MedicineOutsService))
):
    new_medicine = MedicineOutsService.create(medicine_data)

    return new_medicine

@router.get('/', response_model=List[MedicineOutResponse])
def get_all_medicine_out_by_medicine_in_id(
    medicine_filter_data: MedicineOutFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    MedicineOutsService: MedicineOutsService = Depends(get_service(MedicineOutsService))
):
    medicine_outs = MedicineOutsService.get_all(medicine_filter_data, all=True)

    return medicine_outs


@router.get('/{id}', response_model=MedicineOutResponse)
def get_medicine_out_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    MedicineOutsService: MedicineOutsService = Depends(get_service(MedicineOutsService))
):
    medicine_out = MedicineOutsService.get_by_id(id)

    return medicine_out


@router.post('/excel-report/', response_model=List[MedicineOutResponse])
def export_food_out_report(
    medicine_filter_data: MedicineOutFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    MedicineOutsService: MedicineOutsService = Depends(get_service(MedicineOutsService))
):
    if medicine_filter_data.from_date is None and medicine_filter_data.to_date is None:
        medicine_filter_data.to_date = datetime.now()
        medicine_filter_data.from_date  = medicine_filter_data.to_date - timedelta(days=30)

    medicine_out_reports = MedicineOutsService.get_all(medicine_filter_data, False)

    return medicine_out_reports


@router.get('/{pond_id}/history', response_model=List[MedicineOutHistoryResponse])
def get_all_medicine_out_history(
    pond_id: int,
    current_user=Depends(get_authenticated_user),
    MedicineOutsService: MedicineOutsService = Depends(get_service(MedicineOutsService))
):
    medicine_outs = MedicineOutsService.get_medicine_out_history(pond_id)

    return medicine_outs

@router.get('/{pond_id}/quantity')
def get_total_quantity_for_pond(
    pond_id: int,
    current_user=Depends(get_authenticated_user),
    MedicineOutsService: MedicineOutsService = Depends(get_service(MedicineOutsService))
):
    total_quantity = MedicineOutsService.get_total_quantity_medicine_out_for_pond(pond_id)

    return {"total_quantity": total_quantity}

