from fastapi import APIRouter, Depends
from typing import List
from app.schemas.chemistry_out import ChemistryOutCreate, ChemistryOutResponse, ChemistryOutHistoryValue, ChemistryOutHistoryResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.chemistry_out import ChemistryOutService
from app.schemas.chemistry_out import ChemistryOutFilter
from datetime import datetime, timedelta

router = APIRouter(
    prefix='/chemistry-out',
    tags=['Chemistry out']
)


@router.post('/', response_model=ChemistryOutResponse)
def create_chemistry_out(
    chemistry_out_data: ChemistryOutCreate,
    current_user=Depends(get_authenticated_user),
    ChemistryOutService: ChemistryOutService = Depends(get_service(ChemistryOutService))
):
    new_chemistry = ChemistryOutService.create(chemistry_out_data)

    return new_chemistry


@router.get('/', response_model=List[ChemistryOutResponse])
def get_all_chemistry_out_by_chemistry_in_id(
    chemistry_out_filter: ChemistryOutFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    ChemistryOutService: ChemistryOutService = Depends(get_service(ChemistryOutService))
):
    chemistry_outs = ChemistryOutService.get_all(chemistry_out_filter, True)

    return chemistry_outs


@router.get('/{id}', response_model=ChemistryOutResponse)
def get_chemistry_out_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    ChemistryOutService: ChemistryOutService = Depends(get_service(ChemistryOutService))
):
    chemistry_out = ChemistryOutService.get_by_id(id)

    return chemistry_out


@router.post('/excel-report/', response_model=List[ChemistryOutResponse])
def export_chemistry_out_report(
    chemistry_out_export: ChemistryOutFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    ChemistryOutService: ChemistryOutService = Depends(get_service(ChemistryOutService))
):
    if chemistry_out_export.from_date is None and chemistry_out_export.to_date is None:
        chemistry_out_export.to_date = datetime.now()
        chemistry_out_export.from_date  = chemistry_out_export.to_date - timedelta(days=30)

    chemistry_out_reports = ChemistryOutService.get_all(chemistry_out_export, False)

    return chemistry_out_reports



@router.get('/{pond_id}/history', response_model=List[ChemistryOutHistoryResponse])
def get_all_chemistry_out_history(
    pond_id: int,
    current_user=Depends(get_authenticated_user),
    ChemistryOutService: ChemistryOutService = Depends(get_service(ChemistryOutService))
):
    chemistry_outs = ChemistryOutService.get_chemistry_out_history(pond_id)

    return chemistry_outs


@router.get('/{pond_id}/quantity')
def get_total_quantity_for_pond(
    pond_id: int,
    current_user=Depends(get_authenticated_user),
    ChemistryOutService: ChemistryOutService = Depends(get_service(ChemistryOutService))
):
    total_quantity = ChemistryOutService.get_total_quantity_medicine_out_for_pond(pond_id)

    return {"total_quantity": total_quantity}

