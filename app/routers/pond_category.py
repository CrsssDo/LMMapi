from fastapi import APIRouter, Depends
from typing import List
from app.schemas.pond import PondCategorizesResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.pond import PondCategorizesService


router = APIRouter(
    prefix='/pond-category',
    tags=['Pond category']
)


@router.get('/', response_model=List[PondCategorizesResponse])
def get_all_pond_categorizes(
    current_user=Depends(get_authenticated_user),
    PondCategorizesService: PondCategorizesService = Depends(get_service(PondCategorizesService))
):
    pond_categorizes = PondCategorizesService.get_all()

    return pond_categorizes
