from fastapi import APIRouter, Depends, Response, status
from typing import List
from app.schemas.supplier import SupplierCreateRequest, SupplierUpdateRequest, SupplierResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.supplier import SuppliersService


router = APIRouter(
    prefix='/suppliers',
    tags=['Suppliers']
)


@router.post('/', response_model=SupplierResponse)
def create_supplier(
    supplier_data: SupplierCreateRequest,
    current_user=Depends(get_authenticated_user),
    SuppliersService: SuppliersService = Depends(get_service(SuppliersService))
):
    new_supplier = SuppliersService.create(supplier_data)

    return new_supplier


@router.get('/', response_model=List[SupplierResponse])
def get_all_suppliers(
    current_user=Depends(get_authenticated_user),
    SuppliersService: SuppliersService = Depends(get_service(SuppliersService))
):
    suppliers = SuppliersService.get_all()

    return suppliers

@router.patch('/{id}', response_model=SupplierResponse)
def update_supplier(
    id: int,
    supplier_data: SupplierUpdateRequest,
    current_user=Depends(get_authenticated_user),
    SuppliersService: SuppliersService = Depends(get_service(SuppliersService))
):
    supplier_update = SuppliersService.update_supplier(id, supplier_data)

    return supplier_update


@router.get('/{id}', response_model=SupplierResponse)
def get_supplier_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    SuppliersService: SuppliersService = Depends(get_service(SuppliersService))
):
    supplier = SuppliersService.get_by_id(id)

    return supplier


@router.delete('/{id}/soft-delete')
def soft_delete_supplier(
    id: int,
    current_user=Depends(get_authenticated_user),
    SuppliersService: SuppliersService = Depends(get_service(SuppliersService))
):
    SuppliersService.soft_delete_supplier(id)

    return Response(status_code=status.HTTP_200_OK)









