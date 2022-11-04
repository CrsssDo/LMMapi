from fastapi import APIRouter, Depends
from typing import List
from app.schemas.food_out import FoodOutCreateRequest, FoodOutResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.food_out import FoodOutService
from app.schemas.food_out import FoodOutFilter, FoodOutHistoryValue, FoodOutHistoryResponse
from datetime import datetime, timedelta

router = APIRouter(
    prefix='/food-out',
    tags=['Food out']
)


@router.post('/', response_model=FoodOutResponse)
def create_food_out(
    food_out_data: FoodOutCreateRequest,
    current_user=Depends(get_authenticated_user),
    FoodOutService: FoodOutService = Depends(get_service(FoodOutService))
):
    new_food = FoodOutService.create(food_out_data)

    return new_food


@router.get('/', response_model=List[FoodOutResponse])
def get_all_food_out_by_food_in_id(
    food_out_filter: FoodOutFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    FoodOutService: FoodOutService = Depends(get_service(FoodOutService))
):
    food_outs = FoodOutService.get_all(food_out_filter, True)

    return food_outs


@router.get('/{id}', response_model=FoodOutResponse)
def get_food_out_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    FoodOutService: FoodOutService = Depends(get_service(FoodOutService))
):
    food_out = FoodOutService.get_by_id(id)

    return food_out


@router.post('/excel-report/', response_model=List[FoodOutResponse])
def export_food_out_report(
    food_out_export: FoodOutFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    FoodOutService: FoodOutService = Depends(get_service(FoodOutService))
):
    if food_out_export.from_date is None and food_out_export.to_date is None:
        food_out_export.to_date = datetime.now()
        food_out_export.from_date  = food_out_export.to_date - timedelta(days=30)

    food_out_reports = FoodOutService.get_all(food_out_export, False)

    return food_out_reports


@router.get('/{pond_id}/history', response_model=List[FoodOutHistoryResponse])
def get_all_food_out_history(
    pond_id: int,
    current_user=Depends(get_authenticated_user),
    FoodOutService: FoodOutService = Depends(get_service(FoodOutService))
):
    food_outs = FoodOutService.get_food_out_history(pond_id)

    return food_outs

@router.get('/{pond_id}/quantity')
def get_total_quantity_for_pond(
    pond_id: int,
    current_user=Depends(get_authenticated_user),
    FoodOutService: FoodOutService = Depends(get_service(FoodOutService))
):
    total_quantity = FoodOutService.get_total_quantity_food_out_for_pond(pond_id)

    return {"total_quantity": total_quantity}

