from fastapi import APIRouter, Depends, Response, status
from typing import List
from app.core.auth import get_authenticated_user
from app.schemas.purchasing_dealer import PurchasingDealerCreateRequest, PurchasingDealersResponse, PurchasingDealerUpdateRequest
from app.core.service import get_service
from app.services.purchasing_dealer import PurchasingDealersService


router = APIRouter(
    prefix='/purchasing-dealer',
    tags=['Purchasing Dealer']
)


@router.post('/', response_model=PurchasingDealersResponse)
def create_purchasing_dealer(
    purchasing_dealer_data: PurchasingDealerCreateRequest,
    current_user=Depends(get_authenticated_user),
    PurchasingDealersService: PurchasingDealersService = Depends(get_service(PurchasingDealersService))
):
    new_purchasing_dealer = PurchasingDealersService.create(purchasing_dealer_data)

    return new_purchasing_dealer


@router.get('/', response_model=List[PurchasingDealersResponse])
def get_all_purchasing_dealer(
    current_user=Depends(get_authenticated_user),
    PurchasingDealersService: PurchasingDealersService = Depends(get_service(PurchasingDealersService))
):
    purchasing_dealers = PurchasingDealersService.get_all()

    return purchasing_dealers

@router.patch('/{id}', response_model=PurchasingDealersResponse)
def update_purchasing(
    id: int,
    purchasing_dealer_data: PurchasingDealerUpdateRequest,
    current_user=Depends(get_authenticated_user),
    PurchasingDealersService: PurchasingDealersService = Depends(get_service(PurchasingDealersService))
):
    purchasing_update = PurchasingDealersService.update_purchasing_dealer(id, purchasing_dealer_data)

    return purchasing_update


@router.get('/{id}', response_model=PurchasingDealersResponse)
def get_purchasing_dealer_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    PurchasingDealersService: PurchasingDealersService = Depends(get_service(PurchasingDealersService))
):
    purchasing_dealer = PurchasingDealersService.get_by_id(id)

    return purchasing_dealer


@router.delete('/{id}/soft-delete')
def soft_delete_dealer(
    id: int,
    current_user=Depends(get_authenticated_user),
    PurchasingDealersService: PurchasingDealersService = Depends(get_service(PurchasingDealersService))
):
    PurchasingDealersService.soft_delete_dealers(id)

    return Response(status_code=status.HTTP_200_OK)






