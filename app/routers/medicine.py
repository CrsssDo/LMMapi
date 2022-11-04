from fastapi import APIRouter, Depends, Query, Response, status, UploadFile, File
from typing import List
from app.schemas.medicine import MedicineCreateRequest, MedicineUpdateRequest, MedicineStatusUpdateRequest, MedicinesResponse, MedicineDetailResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.medicine import MedicinesService
from app.schemas.image import MedicineImageSubType


router = APIRouter(
    prefix='/medicines',
    tags=['Medicines']
)


@router.post('/', response_model=MedicinesResponse)
def create_medicine(
    medicine_data: MedicineCreateRequest,
    current_user=Depends(get_authenticated_user),
    MedicinesService: MedicinesService = Depends(get_service(MedicinesService))
):
    new_medicine = MedicinesService.create(medicine_data)

    return new_medicine


@router.get('/', response_model=List[MedicinesResponse])
def get_all_medicines(
    status: bool = Query(False),
    current_user=Depends(get_authenticated_user),
    MedicinesService: MedicinesService = Depends(get_service(MedicinesService))
):
    medicines = MedicinesService.get_all(status)

    return medicines

@router.patch('/{id}', response_model=MedicinesResponse)
def update_medicine(
    id: int,
    medicine_data: MedicineUpdateRequest,
    current_user=Depends(get_authenticated_user),
    MedicinesService: MedicinesService = Depends(get_service(MedicinesService))
):
    medicine_update = MedicinesService.update_medicine(id, medicine_data)

    return medicine_update


@router.get('/{id}', response_model=MedicineDetailResponse)
def get_medicine_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    MedicinesService: MedicinesService = Depends(get_service(MedicinesService))
):
    medicine = MedicinesService.get_by_id(id)

    return medicine



@router.patch('/status/{id}', response_model=MedicinesResponse)
def update_medicine_status(
    id: int,
    medicine_status: MedicineStatusUpdateRequest,
    current_user=Depends(get_authenticated_user),
    MedicinesService: MedicinesService = Depends(get_service(MedicinesService))
):
    medicine_status_update = MedicinesService.update_status(id,medicine_status)

    return medicine_status_update


@router.post("/{medicine_id}/image")
def upload_medicine_image(
        medicine_id: int,
        image_data: UploadFile = File(...),
        medicine_subtype: MedicineImageSubType = None,
        current_user=Depends(get_authenticated_user),
        MedicinesService: MedicinesService = Depends(get_service(MedicinesService))
):
    MedicinesService.upload_medicine_image(medicine_id, image_data, medicine_subtype)

    return Response(status_code=status.HTTP_200_OK)


@router.post("/{medicine_id}/images")
def upload_multi_medicine_image(
        medicine_id: int,
        image_datas: List[UploadFile] = File(...),
        medicine_subtype: MedicineImageSubType = None,
        current_user=Depends(get_authenticated_user),
        MedicinesService: MedicinesService = Depends(get_service(MedicinesService))
):
    MedicinesService.upload_multi_medicine_image(medicine_id, image_datas, medicine_subtype)

    return Response(status_code=status.HTTP_200_OK)


@router.delete('/{id}/soft-delete')
def soft_delete_medicine(
    id: int,
    current_user=Depends(get_authenticated_user),
    MedicinesService: MedicinesService = Depends(get_service(MedicinesService))
):
    MedicinesService.soft_delete_medicine(id)

    return Response(status_code=status.HTTP_200_OK)


