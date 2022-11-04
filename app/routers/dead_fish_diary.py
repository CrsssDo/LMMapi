from datetime import date
from typing import List
from fastapi import APIRouter, Depends
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.dead_fish_diary import DeadFishDiariesService
from app.schemas.dead_fish_diary import DeadFishDiaryCreateRequest, DeadFishDiaryResponse, DeadFishDiaryUpdateRequest


router = APIRouter(
    prefix='/dead-fish-diary',
    tags=['Dead fish diary']
)


@router.get('/{pond_id}', response_model=DeadFishDiaryResponse)
def get_dead_fish_diary_by_pond_id(
    pond_id: int,
    current_user=Depends(get_authenticated_user),
    DeadFishDiariesService: DeadFishDiariesService = Depends(get_service(DeadFishDiariesService))
):
    dead_fish_diary = DeadFishDiariesService.get_dead_fish_by_pond_id(pond_id)

    return dead_fish_diary

@router.patch('/', response_model=DeadFishDiaryResponse)
def update_dead_fish_diary(
    id: int,
    dead_fish_diary_update: DeadFishDiaryUpdateRequest,
    current_user=Depends(get_authenticated_user),
    DeadFishDiariesService: DeadFishDiariesService = Depends(get_service(DeadFishDiariesService))
):
    dead_fish_diary = DeadFishDiariesService.update(id, dead_fish_diary_update)

    return dead_fish_diary


@router.get('/', response_model=List[DeadFishDiaryResponse])
def get_all(
    adopt_id: int,
    in_date: date,
    current_user=Depends(get_authenticated_user),
    DeadFishDiariesService: DeadFishDiariesService = Depends(get_service(DeadFishDiariesService))
):
    water_diary = DeadFishDiariesService.get_all(adopt_id, in_date)

    return water_diary


@router.get('/{pond_id}/history', response_model=List[DeadFishDiaryResponse])
def get_dead_fish_diary_history(
    pond_id: int,
    current_user=Depends(get_authenticated_user),
    DeadFishDiariesService: DeadFishDiariesService = Depends(get_service(DeadFishDiariesService))
):
    dead_fish_histories = DeadFishDiariesService.get_dead_fish_diary_history(pond_id)

    return dead_fish_histories


@router.get('/{pond_id}/statistic', response_model=List[DeadFishDiaryResponse])
def get_dead_fish_diary_history(
    from_date: date,
    to_date: date,
    pond_id: int = None,
    current_user=Depends(get_authenticated_user),
    DeadFishDiariesService: DeadFishDiariesService = Depends(get_service(DeadFishDiariesService))
):
    dead_fish_statistics = DeadFishDiariesService.get_dead_fish_by_range_date(pond_id=pond_id , from_date=from_date, to_date=to_date)

    return dead_fish_statistics
