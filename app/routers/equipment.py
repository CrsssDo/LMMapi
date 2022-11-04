from fastapi import APIRouter, Depends, Response, status, UploadFile, File
from typing import List
from app.schemas.equipment import EquipmentResponse, EquipmentCreateRequest, EquipmentUpdateRequest, EquipmentDetailResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.equipment import EquipmentsService


router = APIRouter(
    prefix='/equipments',
    tags=['Equipments']
)


@router.post('/', response_model=EquipmentResponse)
def create_equipment(
    equipment_data: EquipmentCreateRequest,
    current_user=Depends(get_authenticated_user),
    EquipmentsService: EquipmentsService = Depends(get_service(EquipmentsService))
):
    new_equipment = EquipmentsService.create(equipment_data)

    return new_equipment


@router.get('/', response_model=List[EquipmentResponse])
def get_all_equipment(
    current_user=Depends(get_authenticated_user),
    EquipmentsService: EquipmentsService = Depends(get_service(EquipmentsService))
):
    equipment = EquipmentsService.get_all()

    return equipment

@router.patch('/{id}', response_model=EquipmentResponse)
def update_equipment(
    id: int,
    equipment_data: EquipmentUpdateRequest,
    current_user=Depends(get_authenticated_user),
    EquipmentsService: EquipmentsService = Depends(get_service(EquipmentsService))
):
    equipment_update = EquipmentsService.update_equipment(id, equipment_data)

    return equipment_update

@router.get('/{id}', response_model=EquipmentDetailResponse)
def get_equipment_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    EquipmentsService: EquipmentsService = Depends(get_service(EquipmentsService))
):
    equipment = EquipmentsService.get_by_id(id)

    return equipment


@router.post("/{equipment_id}/image")
def upload_equipment_image(
        equipment_id: int,
        image_data: UploadFile = File(...),
        current_user=Depends(get_authenticated_user),
    EquipmentsService: EquipmentsService = Depends(get_service(EquipmentsService))
):
    EquipmentsService.upload_equipment_image(equipment_id , image_data)

    return Response(status_code=status.HTTP_200_OK)


@router.post("/{equipment_id}/images")
def upload_multi_equipment_image(
        equipment_id: int,
        image_datas: List[UploadFile] = File(...),
        current_user=Depends(get_authenticated_user),
    EquipmentsService: EquipmentsService = Depends(get_service(EquipmentsService))
):
    EquipmentsService.upload_multi_equipment_image(equipment_id, image_datas)

    return Response(status_code=status.HTTP_200_OK)


@router.delete('/{id}/soft-delete')
def soft_delete_equipment(
    id: int,
    current_user=Depends(get_authenticated_user),
    EquipmentsService: EquipmentsService = Depends(get_service(EquipmentsService))
):
    EquipmentsService.soft_delete_equipment(id)

    return Response(status_code=status.HTTP_200_OK)




