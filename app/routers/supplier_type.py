from fastapi import APIRouter, Depends, Response, status
from typing import List
from app.schemas.supplier import SuppliersTypeResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.supplier import  SupplierTypesService


router = APIRouter(
    prefix='/supplier-types',
    tags=['Supplier types']
)


@router.get('/', response_model=List[SuppliersTypeResponse])
def get_all_supplier_types(
    current_user=Depends(get_authenticated_user),
    SupplierTypesService: SupplierTypesService = Depends(get_service(SupplierTypesService))
):
    supplier_types = SupplierTypesService.get_all()

    return supplier_types