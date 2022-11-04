from fastapi import APIRouter, Depends
from typing import List
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.environment import EnvironmentsService
from app.schemas.environment import EnvironmentsResponse

router = APIRouter(
    prefix='/environments',
    tags=['Environments']
)


@router.get('/', response_model=List[EnvironmentsResponse])
def get_all_environments(
    current_user=Depends(get_authenticated_user),
    EnvironmentsService: EnvironmentsService = Depends(get_service(EnvironmentsService))
):
    environments = EnvironmentsService.get_all()

    return environments

