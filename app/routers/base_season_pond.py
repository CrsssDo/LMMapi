from fastapi import APIRouter, Body, Depends, Form, Query
from typing import List
from app.schemas.base_season_pond import BaseSeasonPondCreateRequest, BaseSeasonPondResponse, BaseSeasonPondsStatus, BaseSeasonPondsUpdateRequest, BaseSeasonsCompleteUpdateRequest
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.base_season_pond import BaseSeasonPondsService


router = APIRouter(
    prefix='/base-season-ponds',
    tags=['Base season ponds']
)


# @router.get('/', response_model=List[BaseSeasonPondResponse])
# def get_all_base_seasons(
#     adopt_id: int,
#     current_user=Depends(get_authenticated_user),
#     BaseSeasonPondsService: BaseSeasonPondsService = Depends(get_service(BaseSeasonPondsService))
# ):
#     base_seasons = BaseSeasonPondsService.get_all(adopt_id)

#     return base_seasons

@router.patch('/{id}', response_model=BaseSeasonPondResponse)
def update_pond_base_season(
    id: int,
    base_season_update_data: BaseSeasonPondsUpdateRequest,
    current_user=Depends(get_authenticated_user),
    BaseSeasonPondsService: BaseSeasonPondsService = Depends(get_service(BaseSeasonPondsService))
):
    base_season_update = BaseSeasonPondsService.update_pond_base_season(id, base_season_update_data)

    return base_season_update


@router.patch('/{id}/complete', response_model=BaseSeasonPondResponse)
def update_pond_base_season_complete(
    id: int,
    base_season_update_data: BaseSeasonsCompleteUpdateRequest,
    current_user=Depends(get_authenticated_user),
    BaseSeasonPondsService: BaseSeasonPondsService = Depends(get_service(BaseSeasonPondsService))
):
    base_season_update = BaseSeasonPondsService.update_pond_base_season(id, base_season_update_data)

    return base_season_update


@router.get('/{id}', response_model=BaseSeasonPondResponse)
def get_pond_base_season_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    BaseSeasonPondsService: BaseSeasonPondsService = Depends(get_service(BaseSeasonPondsService))
):
    base_season = BaseSeasonPondsService.get_by_id(id)

    return base_season


@router.patch('/{id}/status', response_model=BaseSeasonPondResponse)
def update_pond_base_season_status(
    id: int,
    base_season_status_data: BaseSeasonPondsStatus = Body(...),
    current_user=Depends(get_authenticated_user),
    BaseSeasonPondsService: BaseSeasonPondsService = Depends(get_service(BaseSeasonPondsService))
):
    base_season_update = BaseSeasonPondsService.update_status(id, base_season_status_data)

    return base_season_update




