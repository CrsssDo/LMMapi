from fastapi import APIRouter, Depends, Form, Response, status
from typing import List
from app.schemas.water_diary_detail import WaterDiaryDetailCreateRequest
from app.schemas.water_diary import WaterDiariesReportResponse, WaterDiaryCreateRequest, WaterDiaryFilter, WaterDiaryResponse, WaterDiaryCommentCreateRequest
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.water_diary import WaterDiariesService


router = APIRouter(
    prefix='/water-diary',
    tags=['Water diary']
)


@router.post('/', response_model=WaterDiaryResponse)
def create_water_diary(
    water_diary_data: WaterDiaryCreateRequest,
    current_user=Depends(get_authenticated_user),
    WaterDiariesService: WaterDiariesService = Depends(get_service(WaterDiariesService))
):
    new_water_diary = WaterDiariesService.create(water_diary_data)

    return new_water_diary


@router.get('/', response_model=List[WaterDiaryResponse])
def get_water_diary_by_pond_id(
    filter_data: WaterDiaryFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    WaterDiariesService: WaterDiariesService = Depends(get_service(WaterDiariesService))
):
    water_diaries = WaterDiariesService.get_water_diary_by_pond_id(filter_data)

    return water_diaries


@router.patch('/', response_model=WaterDiaryResponse)
def update_water_measure_value(
    id: int,
    water_diary_comment: WaterDiaryCommentCreateRequest,
    water_diary_detail_data: List[WaterDiaryDetailCreateRequest],
    current_user=Depends(get_authenticated_user),
    WaterDiariesService: WaterDiariesService = Depends(get_service(WaterDiariesService))
):
    water_diary= WaterDiariesService.update(id, water_diary_detail_data, water_diary_comment)

    return water_diary


@router.get('/{id}', response_model=WaterDiaryResponse)
def get_water_diary_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    WaterDiariesService: WaterDiariesService = Depends(get_service(WaterDiariesService))
):
    water_diary_out = WaterDiariesService.get_by_id(id)

    return water_diary_out


@router.get('/{pond_id}/history/')
def get_history_water_diary(
    pond_id: int,
    current_user=Depends(get_authenticated_user),
    WaterDiariesService: WaterDiariesService = Depends(get_service(WaterDiariesService))
):
    history_water_diaries = WaterDiariesService.get_water_history_by_pond_id(pond_id)

    return history_water_diaries


@router.get('/report/', response_model=List[WaterDiariesReportResponse])
def report_water_diaries(
    filter_data: WaterDiaryFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    WaterDiariesService: WaterDiariesService = Depends(get_service(WaterDiariesService))
):
    water_diaries = WaterDiariesService.report_water_diaries(filter_data)

    return water_diaries



