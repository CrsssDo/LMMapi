from fastapi import APIRouter, Depends
from typing import List
from app.schemas.adopt import  AdoptsTypeResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.adopt import  AdoptTypesService


router = APIRouter(
    prefix='/adopt-types',
    tags=['Adopt types']
)


@router.get('/', response_model=List[AdoptsTypeResponse])
def get_all_adopt_types(
    current_user=Depends(get_authenticated_user),
    AdoptTypesService: AdoptTypesService = Depends(get_service(AdoptTypesService))
):
    adopt_types = AdoptTypesService.get_all()

    return adopt_types
