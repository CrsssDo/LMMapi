from fastapi import APIRouter, Depends, Query, Response, status, UploadFile, File
from typing import List
from app.schemas.chemistry import ChemistryCreateRequest, ChemistryUpdateRequest, ChemistryStatusUpdateRequest, ChemistryResponse, ChemistryDetailResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.chemistry import ChemistriesService
from app.schemas.image import ChemistryImageSubType


router = APIRouter(
    prefix='/chemistry',
    tags=['Chemistry']
)


@router.post('/', response_model=ChemistryResponse)
def create_chemistry(
    chemistry_data: ChemistryCreateRequest,
    current_user=Depends(get_authenticated_user),
    ChemistriesService: ChemistriesService = Depends(get_service(ChemistriesService))
):
    new_chemistry = ChemistriesService.create(chemistry_data)

    return new_chemistry


@router.get('/', response_model=List[ChemistryResponse])
def get_all_chemistries(
    status: bool = Query(False),
    current_user=Depends(get_authenticated_user),
    ChemistriesService: ChemistriesService = Depends(get_service(ChemistriesService))
):
    chemistries = ChemistriesService.get_all(status)

    return chemistries

@router.patch('/{id}', response_model=ChemistryResponse)
def update_chemistry(
    id: int,
    chemistry_data: ChemistryUpdateRequest,
    current_user=Depends(get_authenticated_user),
    ChemistriesService: ChemistriesService = Depends(get_service(ChemistriesService))
):
    chemistry_update = ChemistriesService.update_chemistry(id, chemistry_data)

    return chemistry_update


@router.get('/{id}', response_model=ChemistryDetailResponse)
def get_chemistry_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    ChemistriesService: ChemistriesService = Depends(get_service(ChemistriesService))
):
    chemistry = ChemistriesService.get_by_id(id)

    return chemistry


@router.patch('/status/{id}', response_model=ChemistryResponse)
def update_chemistry_status(
    id: int,
    chemistry_status: ChemistryStatusUpdateRequest,
    current_user=Depends(get_authenticated_user),
    ChemistriesService: ChemistriesService = Depends(get_service(ChemistriesService))
):
    chemistry_status_update = ChemistriesService.update_status(id, chemistry_status)

    return chemistry_status_update


@router.post("/{chemistry_id}/image")
def upload_chemistry_image(
        chemistry_id: int,
        image_data: UploadFile = File(...),
        chemistry_subtype: ChemistryImageSubType = None,
        current_user=Depends(get_authenticated_user),
        ChemistriesService: ChemistriesService = Depends(get_service(ChemistriesService))
):
    ChemistriesService.upload_chemistry_image(chemistry_id, image_data, chemistry_subtype)

    return Response(status_code=status.HTTP_200_OK)


@router.post("/{chemistry_id}/images")
def upload_multi_chemistry_image(
        chemistry_id: int,
        image_datas: List[UploadFile] = File(...),
        chemistry_subtype: ChemistryImageSubType = None,
        current_user=Depends(get_authenticated_user),
        ChemistriesService: ChemistriesService = Depends(get_service(ChemistriesService))
):
    ChemistriesService.upload_multi_chemistry_image(chemistry_id, image_datas, chemistry_subtype)

    return Response(status_code=status.HTTP_200_OK)


@router.delete('/{id}/soft-delete')
def soft_delete_chemistry(
    id: int,
    current_user=Depends(get_authenticated_user),
    ChemistriesService: ChemistriesService = Depends(get_service(ChemistriesService))
):
    ChemistriesService.soft_delete_chemistry(id)

    return Response(status_code=status.HTTP_200_OK)


