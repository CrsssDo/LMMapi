from fastapi import APIRouter, Depends, Response, status, UploadFile, File, Body
from typing import List
from app.schemas.food_type import FoodTypesResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.food_type import FoodTypesService


router = APIRouter(
    prefix='/food-types',
    tags=['Food types']
)


@router.post('/', response_model=FoodTypesResponse)
def create_food_type(
    name: str = Body(...),
    current_user=Depends(get_authenticated_user),
    FoodTypesService: FoodTypesService = Depends(get_service(FoodTypesService))
):
    new_food_type = FoodTypesService.create(name)

    return new_food_type


@router.get('/', response_model=List[FoodTypesResponse])
def get_all_food_type(
    current_user=Depends(get_authenticated_user),
    FoodTypesService: FoodTypesService = Depends(get_service(FoodTypesService))
):
    food_type = FoodTypesService.get_all()

    return food_type

@router.patch('/{id}', response_model=FoodTypesResponse)
def update_food_type(
    id: int,
    name: str = Body(...),
    current_user=Depends(get_authenticated_user),
    FoodTypesService: FoodTypesService = Depends(get_service(FoodTypesService))
):
    food_type_update = FoodTypesService.update_food_type(id, name)

    return food_type_update


@router.get('/{id}', response_model=FoodTypesResponse)
def get_food_type_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    FoodTypesService: FoodTypesService = Depends(get_service(FoodTypesService))
):
    food_type = FoodTypesService.get_by_id(id)

    return food_type


@router.delete('/{id}/soft-delete')
def soft_delete_food_type(
    id: int,
    current_user=Depends(get_authenticated_user),
    FoodTypesService: FoodTypesService = Depends(get_service(FoodTypesService))
):
    FoodTypesService.soft_delete_food_type(id)

    return Response(status_code=status.HTTP_200_OK)









