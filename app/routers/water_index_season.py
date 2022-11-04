from fastapi import APIRouter, Body, Depends
from typing import List
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.schemas.water_index_season import WaterIndexSeasonCreateRequest, WaterIndexSeasonUpdateRequest, WaterIndexSeasonResponse
from app.services.water_index_season import WaterIndexSeasonsService


router = APIRouter(
    prefix='/water-index-season',
    tags=['Water index season']
)


@router.post('/', response_model=WaterIndexSeasonResponse)
def create_water_index_season(
    water_index_season_data: WaterIndexSeasonCreateRequest,
    current_user=Depends(get_authenticated_user),
    WaterIndexSeasonsService: WaterIndexSeasonsService = Depends(get_service(WaterIndexSeasonsService))
):
    new_water_index_season = WaterIndexSeasonsService.create(water_index_season_data)

    return new_water_index_season


@router.patch('/{base_season_id}', response_model=WaterIndexSeasonResponse)
def update_water_index_season_value(
    base_season_id: int,
    water_index_season_data: List[WaterIndexSeasonUpdateRequest],
    water_index_poison: str = Body(None),
    current_user=Depends(get_authenticated_user),
    WaterIndexSeasonsService: WaterIndexSeasonsService = Depends(get_service(WaterIndexSeasonsService))
):
    water_index_season_update = WaterIndexSeasonsService.update(base_season_id, water_index_season_data, water_index_poison)

    return water_index_season_update


@router.patch('/{base_season_id}/complete', response_model=WaterIndexSeasonResponse)
def update_water_index_season_value_complete(
    base_season_id: int,
    water_index_season_data: List[WaterIndexSeasonUpdateRequest],
    water_index_poison: str = Body(...),
    current_user=Depends(get_authenticated_user),
    WaterIndexSeasonsService: WaterIndexSeasonsService = Depends(get_service(WaterIndexSeasonsService))
):
    water_index_season_update = WaterIndexSeasonsService.update(base_season_id, water_index_season_data, water_index_poison)

    return water_index_season_update

