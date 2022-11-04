from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from typing import List

from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.food_in import FoodInService
from app.schemas.food_in import FoodInResponse, FoodInFilter, FoodInCreateRequest, FoodInUpdateRequest


router = APIRouter(
    prefix='/food-in',
    tags=['Food in']
)


@router.post('/', response_model=FoodInResponse)
def create_food_in(
    food_in_data: FoodInCreateRequest,
    current_user=Depends(get_authenticated_user),
    FoodInService: FoodInService = Depends(get_service(FoodInService))
):
    new_food = FoodInService.create(food_in_data)

    return new_food


@router.get('/', response_model=List[FoodInResponse])
def get_all_food_in_by_food_id(
    food_filter_data: FoodInFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    FoodInService: FoodInService = Depends(get_service(FoodInService))
):
    food_ins = FoodInService.get_all(food_filter_data, True)

    return food_ins


@router.get('/{id}', response_model=FoodInResponse)
def get_food_in_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    FoodInService: FoodInService = Depends(get_service(FoodInService))
):
    food_in = FoodInService.get_by_id(id)

    return food_in


@router.post('/excel-report/', response_model=List[FoodInResponse])
def export_food_in_report(
    food_filter_data: FoodInFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    FoodInService: FoodInService = Depends(get_service(FoodInService))
):
    if food_filter_data.from_date is None and food_filter_data.to_date is None:
        food_filter_data.to_date = datetime.now()
        food_filter_data.from_date  = food_filter_data.to_date - timedelta(days=30)

    food_in_report = FoodInService.get_all(food_filter_data, False)

    return food_in_report


@router.patch('/{id}', response_model=FoodInResponse)
def update_food_in_by_id(
    id: int,
    food_in_update_data: FoodInUpdateRequest,
    current_user=Depends(get_authenticated_user),
    FoodInService: FoodInService = Depends(get_service(FoodInService))
):
    food_in = FoodInService.update(id, food_in_update_data)

    return food_in

