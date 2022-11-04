from fastapi import APIRouter, Body, Depends, Form, Query, Response, status
from typing import List
from app.schemas.collect_season import CollectSeasonCreateRequest, CollectSeasonResponse, CollectSeasonUpdateRequest, CollectSeasonCompleteUpdateRequest
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.collect_season import CollectSeasonsService


router = APIRouter(
    prefix='/collect-season',
    tags=['Collect seasons']
)


@router.get('/{base_season_id}', response_model=CollectSeasonResponse)
def get_collect_seasons_by_base_season_id(
    base_season_id: int,
    current_user=Depends(get_authenticated_user),
    CollectSeasonsService: CollectSeasonsService = Depends(get_service(CollectSeasonsService))
):
    collect_seasons = CollectSeasonsService.get_collect_season_by_base_season_id(base_season_id)

    return collect_seasons

@router.patch('/{id}', response_model=CollectSeasonResponse)
def update_collect_season(
    id: int,
    collect_season_update_data: CollectSeasonUpdateRequest,
    current_user=Depends(get_authenticated_user),
    CollectSeasonsService: CollectSeasonsService = Depends(get_service(CollectSeasonsService))
):
    collect_season_update = CollectSeasonsService.update_collect_season(id, collect_season_update_data)

    return collect_season_update


@router.patch('/{id}/complete', response_model=CollectSeasonResponse)
def update_collect_season_complete(
    id: int,
    collect_season_update_data: CollectSeasonCompleteUpdateRequest,
    current_user=Depends(get_authenticated_user),
    CollectSeasonsService: CollectSeasonsService = Depends(get_service(CollectSeasonsService))
):
    collect_season_update = CollectSeasonsService.update_collect_season(id, collect_season_update_data)

    return collect_season_update

    