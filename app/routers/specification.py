from typing import List
from app.schemas.specification import SpecificationCreateForm, SpecificationResponse, SpecificationFilter
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.specification import SpecificationsService
from fastapi import APIRouter, Depends, Response, status, UploadFile, File

router = APIRouter(
    prefix='/specifications',
    tags=['Specifications']
)


@router.post('/', response_model=SpecificationResponse)
def create_specification(
    specification_data: SpecificationCreateForm = Depends(),
    current_user=Depends(get_authenticated_user),
    SpecificationsService: SpecificationsService = Depends(get_service(SpecificationsService))
):
    new_specification = SpecificationsService.create(specification_data)

    return new_specification


@router.get('/', response_model=List[SpecificationResponse])
def get_all_specifications(
    specification_filter: SpecificationFilter = Depends(),
    current_user=Depends(get_authenticated_user),
    SpecificationsService: SpecificationsService = Depends(get_service(SpecificationsService))
):
    specifications = SpecificationsService.get_all(specification_filter)

    return specifications


@router.get('/{id}', response_model=SpecificationResponse)
def get_specification_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    SpecificationsService: SpecificationsService = Depends(get_service(SpecificationsService))
):
    specification = SpecificationsService.get_by_id(id)

    return specification

@router.post("/{specification_id}/image")
def upload_specification_image(
    specification_id: int,
    image_data: UploadFile = File(...),
    current_user=Depends(get_authenticated_user),
    SpecificationsService: SpecificationsService = Depends(get_service(SpecificationsService))
):
    SpecificationsService.upload_specification_image(specification_id, image_data)

    return Response(status_code=status.HTTP_200_OK)


@router.delete('/{id}/soft-delete')
def soft_delete_specification(
    id: int,
    current_user=Depends(get_authenticated_user),
    SpecificationsService: SpecificationsService = Depends(get_service(SpecificationsService))
):
    SpecificationsService.soft_delete_specification(id)

    return Response(status_code=status.HTTP_200_OK)








