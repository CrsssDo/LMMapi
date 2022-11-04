from fastapi import APIRouter, Depends, Response, status, UploadFile, File
from typing import List
from app.schemas.disease import DiseaseCreateRequest, DiseaseUpdateRequest, DiseaseResponse, DiseaseDetailResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.disease import DiseasesService


router = APIRouter(
    prefix='/fish-disease',
    tags=['Diseases']
)


@router.post('/', response_model=DiseaseResponse)
def create_fish_disease(
    disease_data: DiseaseCreateRequest,
    current_user=Depends(get_authenticated_user),
    DiseasesService: DiseasesService = Depends(get_service(DiseasesService))
):
    new_disease = DiseasesService.create(disease_data)

    return new_disease


@router.get('/', response_model=List[DiseaseResponse])
def get_all_fish_diseases(
    current_user=Depends(get_authenticated_user),
    DiseasesService: DiseasesService = Depends(get_service(DiseasesService))
):
    diseases = DiseasesService.get_all()

    return diseases

@router.patch('/{id}', response_model=DiseaseResponse)
def update_fish_disease(
    id: int,
    disease_data: DiseaseUpdateRequest,
    current_user=Depends(get_authenticated_user),
    DiseasesService: DiseasesService = Depends(get_service(DiseasesService))
):
    disease_update = DiseasesService.update_fish_diseases(id, disease_data)

    return disease_update

@router.get('/{id}', response_model=DiseaseDetailResponse)
def get_fish_disease_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    DiseasesService: DiseasesService = Depends(get_service(DiseasesService))
):
    disease = DiseasesService.get_by_id(id)

    return disease


@router.post("/{disease_id}/image")
def upload_disease_image(
        disease_id: int,
        image_data: UploadFile = File(...),
        current_user=Depends(get_authenticated_user),
        DiseasesService: DiseasesService = Depends(get_service(DiseasesService))
):
    DiseasesService.upload_disease_image(disease_id, image_data)

    return Response(status_code=status.HTTP_200_OK)


@router.post("/{disease_id}/images")
def upload_multi_disease_image(
        disease_id: int,
        image_datas: List[UploadFile] = File(...),
        current_user=Depends(get_authenticated_user),
        DiseasesService: DiseasesService = Depends(get_service(DiseasesService))
):
    DiseasesService.upload_multi_disease_image(disease_id, image_datas)

    return Response(status_code=status.HTTP_200_OK)


@router.delete('/{id}/soft-delete')
def soft_delete_disease(
    id: int,
    current_user=Depends(get_authenticated_user),
    DiseasesService: DiseasesService = Depends(get_service(DiseasesService))
):
    DiseasesService.soft_delete_disease(id)

    return Response(status_code=status.HTTP_200_OK)





