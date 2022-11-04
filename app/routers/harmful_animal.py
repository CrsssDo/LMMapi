from fastapi import APIRouter, Depends, Response, status, UploadFile, File
from typing import List
from app.schemas.harmful_animal import HarmfulAnimalsResponse, HarmfulAnimalCreateRequest, HarmfulAnimalDetailResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.harmful_animal import HarmfulAnimalsService


router = APIRouter(
    prefix='/harmful-animals',
    tags=['Harmful animals']
)


@router.post('/', response_model=HarmfulAnimalsResponse)
def create_animal(
    animal_data: HarmfulAnimalCreateRequest,
    current_user=Depends(get_authenticated_user),
    HarmfulAnimalsService: HarmfulAnimalsService = Depends(get_service(HarmfulAnimalsService))
):
    new_animal = HarmfulAnimalsService.create(animal_data)

    return new_animal


@router.get('/', response_model=List[HarmfulAnimalsResponse])
def get_all_harmful_animal(
    current_user=Depends(get_authenticated_user),
    HarmfulAnimalsService: HarmfulAnimalsService = Depends(get_service(HarmfulAnimalsService))
):
    animal = HarmfulAnimalsService.get_all()

    return animal

@router.patch('/{id}', response_model=HarmfulAnimalsResponse)
def update_animal(
    id: int,
    animal_data: HarmfulAnimalCreateRequest,
    current_user=Depends(get_authenticated_user),
    HarmfulAnimalsService: HarmfulAnimalsService = Depends(get_service(HarmfulAnimalsService))
):
    animal_update = HarmfulAnimalsService.update_harmful_animal(id, animal_data)

    return animal_update


@router.get('/{id}', response_model=HarmfulAnimalDetailResponse)
def get_animal_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    HarmfulAnimalsService: HarmfulAnimalsService = Depends(get_service(HarmfulAnimalsService))
):
    animal = HarmfulAnimalsService.get_by_id(id)

    return animal
    

@router.post("/{animal_id}/image")
def upload_animal_image(
        animal_id: int,
        image_data: UploadFile = File(...),
        current_user=Depends(get_authenticated_user),
        HarmfulAnimalsService: HarmfulAnimalsService = Depends(get_service(HarmfulAnimalsService))
):
    HarmfulAnimalsService.upload_animal_image(animal_id , image_data)

    return Response(status_code=status.HTTP_200_OK)


@router.post("/{animal_id}/images")
def upload_multi_animal_image(
        animal_id: int,
        image_datas: List[UploadFile] = File(...),
        current_user=Depends(get_authenticated_user),
        HarmfulAnimalsService: HarmfulAnimalsService = Depends(get_service(HarmfulAnimalsService))
):
    HarmfulAnimalsService.upload_multi_animal_image(animal_id, image_datas)

    return Response(status_code=status.HTTP_200_OK)

@router.delete('/{id}/soft-delete')
def soft_delete_animal(
    id: int,
    current_user=Depends(get_authenticated_user),
    HarmfulAnimalsService: HarmfulAnimalsService = Depends(get_service(HarmfulAnimalsService))
):
    HarmfulAnimalsService.soft_delete_animal(id)

    return Response(status_code=status.HTTP_200_OK)





