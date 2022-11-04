from fastapi import APIRouter, Depends, Response, status
from typing import List
from app.schemas.address import AddressLevel3Response, AddressLevel2Response, AddressLevel1Response
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.address import AddressService


router = APIRouter(
    tags=['Addresses']
)


@router.get('/address-level-3/', response_model=List[AddressLevel3Response])
def get_all_address_level_3(
    current_user=Depends(get_authenticated_user),
    AddressService: AddressService = Depends(get_service(AddressService))
):
    address_level_3s = AddressService.get_all_address_lv3()

    return address_level_3s


@router.get('/address-level-2/{id}', response_model=List[AddressLevel2Response])
def get_address_level_2_by_address_level_3(
    id: int,
    current_use=Depends(get_authenticated_user),
    AddressService: AddressService = Depends(get_service(AddressService))
):
    address_level_2s = AddressService.get_address_lv2_by_address_lv3_id(id)

    return address_level_2s


@router.get('/address-level-1/{id}', response_model=List[AddressLevel1Response])
def get_address_level_1_by_address_level_2(
    id: int,
    current_user=Depends(get_authenticated_user),
    AddressService: AddressService = Depends(get_service(AddressService))
):
    address_level_1s = AddressService.get_address_lv1_by_address_lv2_id(id)

    return address_level_1s

