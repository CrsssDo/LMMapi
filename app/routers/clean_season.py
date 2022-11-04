from fastapi import APIRouter, Body, Depends, Form, Query, Response, status
from typing import List
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.clean_season import CleanSeasonsService
from app.schemas.clean_season import CleanSeasonCreateRequest, CleanSeasonResponse, CleanSeasonUpdateRequest, CleanSeasonCompleteUpdateRequest


router = APIRouter(
    prefix='/clean-season',
    tags=['Clean seasons']
)

@router.get('/{base_season_id}', response_model=CleanSeasonResponse)
def get_clean_season_by_base_season_id(
    base_season_id: int,
    current_user=Depends(get_authenticated_user),
    CleanSeasonsService: CleanSeasonsService = Depends(get_service(CleanSeasonsService))
):
    clean_season = CleanSeasonsService.get_clean_season_by_base_season_id(base_season_id)

    return clean_season


@router.patch('/{id}', response_model=CleanSeasonResponse)
def update_clean_season(
    id: int,
    clean_season_update_data: CleanSeasonUpdateRequest,
    current_user=Depends(get_authenticated_user),
    CleanSeasonsService: CleanSeasonsService = Depends(get_service(CleanSeasonsService))
):
    clean_season_update = CleanSeasonsService.update_clean_season(id, clean_season_update_data)

    return clean_season_update


@router.patch('/{id}/complete', response_model=CleanSeasonResponse)
def update_clean_season_complete(
    id: int,
    clean_season_update_data: CleanSeasonCompleteUpdateRequest,
    current_user=Depends(get_authenticated_user),
    CleanSeasonsService: CleanSeasonsService = Depends(get_service(CleanSeasonsService))
):
    clean_season_update = CleanSeasonsService.update_clean_season(id, clean_season_update_data)

    return clean_season_update
