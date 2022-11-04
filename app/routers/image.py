from fastapi import APIRouter, Depends, Response, status
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.image import ImagesService


router = APIRouter(
    prefix='/images',
    tags=['Images']
)


@router.delete('/{id}')
def delete_image(
    id: int,
    current_user=Depends(get_authenticated_user),
    ImagesService: ImagesService = Depends(get_service(ImagesService))
):
    ImagesService.delete_image(id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)







