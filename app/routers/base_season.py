from fastapi import APIRouter, Body, Depends, Form, Query
from typing import List
from app.schemas.base_season import BaseSeasonCreateRequest, BaseSeasonStatus, BaseSeasonResponse, BaseSeasonListResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.base_season import BaseSeasonsService


router = APIRouter(
    prefix='/base-seasons',
    tags=['Base seasons']
)


@router.post('/')
def create_base_season(
    base_season_data: BaseSeasonCreateRequest,
    current_user=Depends(get_authenticated_user),
    BaseSeasonsService: BaseSeasonsService = Depends(get_service(BaseSeasonsService))
):
    new_base_season = BaseSeasonsService.create(base_season_data)

    return new_base_season


@router.get('/', response_model=List[BaseSeasonListResponse])
def get_all_base_seasons(
    adopt_id: int = None,
    current_user=Depends(get_authenticated_user),
    BaseSeasonsService: BaseSeasonsService = Depends(get_service(BaseSeasonsService))
):
    base_seasons = BaseSeasonsService.get_all(adopt_id)

    return base_seasons


@router.get('/{id}', response_model=BaseSeasonResponse)
def get_base_season_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    BaseSeasonsService: BaseSeasonsService = Depends(get_service(BaseSeasonsService))
):
    base_season = BaseSeasonsService.get_by_id(id)

    return base_season


@router.patch('/{id}', response_model=BaseSeasonResponse)
def update_base_season_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    BaseSeasonsService: BaseSeasonsService = Depends(get_service(BaseSeasonsService))
):
    base_season = BaseSeasonsService.update_status(id)

    return base_season


@router.post('/{id}', response_model=BaseSeasonResponse)
def create_pond_season_into_base_season(
    id: int,
    pond_list: List = [],
    current_user=Depends(get_authenticated_user),
    BaseSeasonsService: BaseSeasonsService = Depends(get_service(BaseSeasonsService))
):
    base_season = BaseSeasonsService.create_pond_season_into_already_exist_base_season(id, pond_list)

    return base_season


@router.get('/{id}/processing')
def get_processing_bar(
    id: int,
    current_user=Depends(get_authenticated_user),
    BaseSeasonsService: BaseSeasonsService = Depends(get_service(BaseSeasonsService))
):
    processing_value = BaseSeasonsService.get_processing_bar(id)

    return {"processing_value": processing_value}

