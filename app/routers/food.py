from fastapi import APIRouter, Depends, Response, status, UploadFile, File
from typing import List
from app.schemas.food import FoodCreateRequest, FoodUpdateRequest, FoodResponse, FoodDetailResponse, FoodStatusUpdateRequest
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.food import FoodsService
from app.schemas.image import FoodImageSubType


router = APIRouter(
    prefix='/fish-foods',
    tags=['Food']
)


@router.post('/', response_model=FoodResponse)
def create_fish_food(
    food_data: FoodCreateRequest,
    current_user=Depends(get_authenticated_user),
    FoodsService: FoodsService = Depends(get_service(FoodsService))
):
    new_food = FoodsService.create(food_data)

    return new_food


@router.get('/', response_model=List[FoodResponse])
def get_all_fish_foods(
    pond_id: int = None,
    current_user=Depends(get_authenticated_user),
    FoodsService: FoodsService = Depends(get_service(FoodsService))
):
    fish_foods = FoodsService.get_all(pond_id=pond_id)

    return fish_foods

@router.patch('/{id}', response_model=FoodResponse)
def update_fish_food(
    id: int,
    food_data: FoodUpdateRequest,
    current_user=Depends(get_authenticated_user),
    FoodsService: FoodsService = Depends(get_service(FoodsService))
):
    food_update = FoodsService.update_fish_food(id, food_data)

    return food_update


@router.get('/{id}', response_model=FoodDetailResponse)
def get_fish_food_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    FoodsService: FoodsService = Depends(get_service(FoodsService))
):
    food = FoodsService.get_by_id(id)

    return food


@router.patch('/status/{id}', response_model=FoodResponse)
def update_medicine_status(
    id: int,
    food_status: FoodStatusUpdateRequest,
    current_user=Depends(get_authenticated_user),
    FoodsService: FoodsService = Depends(get_service(FoodsService))
):
    food_status_update = FoodsService.update_status(id,food_status)

    return food_status_update


@router.post("/{food_id}/image")
def upload_food_image(
        food_id: int,
        image_data: UploadFile = File(...),
        food_subtype: FoodImageSubType = None,
        current_user=Depends(get_authenticated_user),
        FoodsService: FoodsService = Depends(get_service(FoodsService))
):
    FoodsService.upload_food_image(food_id , image_data, food_subtype)

    return Response(status_code=status.HTTP_200_OK)


@router.post("/{food_id}/images")
def upload_multi_food_image(
        food_id: int,
        image_datas: List[UploadFile] = File(...),
        food_subtype: FoodImageSubType = None,
        current_user=Depends(get_authenticated_user),
        FoodsService: FoodsService = Depends(get_service(FoodsService))
):
    FoodsService.upload_multi_food_image(food_id, image_datas, food_subtype)

    return Response(status_code=status.HTTP_200_OK)


@router.delete('/{id}/soft-delete')
def soft_delete_food(
    id: int,
    current_user=Depends(get_authenticated_user),
    FoodsService: FoodsService = Depends(get_service(FoodsService))
):
    FoodsService.soft_delete_food(id)

    return Response(status_code=status.HTTP_200_OK)




