from fastapi import APIRouter, Depends, Response, status, UploadFile, File
from typing import List, Optional
from app.schemas.pond import PondUpdateRequest, PondCreateRequest, PondsResponse, PondStatusUpdateRequest, PondDetailResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.pond import PondsService


router = APIRouter(
    prefix='/ponds',
    tags=['Ponds']
)


@router.post('/', response_model=PondsResponse)
def create_pond(
    pond_data: PondCreateRequest,
    current_user=Depends(get_authenticated_user),
    PondsService: PondsService = Depends(get_service(PondsService))
):
    new_pond = PondsService.create(pond_data)

    return new_pond


@router.get('/', response_model=List[PondsResponse])
def get_all_ponds(
    adopt_id: Optional[int] = None,
    pond_status: Optional[bool] = False,
    pond_in_base_season: Optional[bool] = False,
    base_season: Optional[bool] = False,
    current_user=Depends(get_authenticated_user),
    PondsService: PondsService = Depends(get_service(PondsService))
):
    ponds = PondsService.get_all(adopt_id=adopt_id, pond_status=pond_status, pond_in_base_season=pond_in_base_season, base_season=base_season)

    return ponds

@router.patch('/{id}', response_model=PondsResponse)
def update_pond(
    id: int,
    pond_data: PondUpdateRequest,
    current_user=Depends(get_authenticated_user),
    PondsService: PondsService = Depends(get_service(PondsService))
):
    pond_update = PondsService.update_pond(id, pond_data)

    return pond_update
    

@router.get('/{id}', response_model=PondDetailResponse)
def get_pond_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    PondsService: PondsService = Depends(get_service(PondsService))
):
    pond = PondsService.get_by_id(id)

    return pond

@router.get('/{pond_type_id}/number-order')
def get_number_order_by_pond_type(
    pond_type_id: int,
    adopt_id: int,
    pond_id: Optional[int] = None,
    current_user=Depends(get_authenticated_user),
    PondsService: PondsService = Depends(get_service(PondsService))
):
    numer_order = PondsService.get_numer_order_by_pond_type(pond_type_id=pond_type_id, adopt_id=adopt_id, pond_id=pond_id)

    return numer_order

@router.get('/{fish_type_id}/fish-type', response_model=List[PondsResponse])
def get_pond_by_fish_type(
    adopt_id: int,
    fish_type_id: int,
    current_user=Depends(get_authenticated_user),
    PondsService: PondsService = Depends(get_service(PondsService))
):
    ponds = PondsService.get_pond_by_fish_type(adopt_id, fish_type_id)

    return ponds


@router.get('/{adopt_id}/adopt-area', response_model=List[PondsResponse])
def get_pond_by_adopt_area_id(
    adopt_id: Optional[int] = None,
    pond_status: Optional[bool] = False,
    current_user=Depends(get_authenticated_user),
    PondsService: PondsService = Depends(get_service(PondsService))
):
    ponds = PondsService.get_all(adopt_id, pond_status)

    return ponds



@router.patch('/status/{id}', response_model=PondsResponse)
def update_pond_status(
    id: int,
    pond_status: PondStatusUpdateRequest,
    current_user=Depends(get_authenticated_user),
    PondsService: PondsService = Depends(get_service(PondsService))
):
    pond_status_update = PondsService.update_status(id, pond_status)

    return pond_status_update


@router.post("/{pond_id}/image")
def upload_pond_image(
        pond_id: int,
        image_data: UploadFile = File(...),
        current_user=Depends(get_authenticated_user),
        PondsService: PondsService = Depends(get_service(PondsService))
):
    PondsService.upload_pond_image(pond_id, image_data)

    return Response(status_code=status.HTTP_200_OK)


@router.post("/{pond_id}/images")
def upload_multi_pond_image(
        pond_id: int,
        image_datas: List[UploadFile] = File(...),
        current_user=Depends(get_authenticated_user),
        PondsService: PondsService = Depends(get_service(PondsService))
):
    PondsService.upload_multi_pond_image(pond_id, image_datas)

    return Response(status_code=status.HTTP_200_OK)



