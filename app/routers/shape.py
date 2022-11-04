from fastapi import APIRouter, Depends, Response, status, UploadFile, File, Body
from typing import List
from app.schemas.shape import ShapeResponse
from app.core.auth import get_authenticated_user
from app.core.service import get_service
from app.services.shape import ShapesService


router = APIRouter(
    prefix='/shapes',
    tags=['Shapes']
)


@router.post('/', response_model=ShapeResponse)
def create_shape(
    name: str = Body(...),
    current_user=Depends(get_authenticated_user),
    ShapesService: ShapesService = Depends(get_service(ShapesService))
):
    new_shape = ShapesService.create(name)

    return new_shape


@router.get('/', response_model=List[ShapeResponse])
def get_all_shape(
    current_user=Depends(get_authenticated_user),
    ShapesService: ShapesService = Depends(get_service(ShapesService))
):
    shape = ShapesService.get_all()

    return shape

@router.patch('/{id}', response_model=ShapeResponse)
def update_shape(
    id: int,
    name: str = Body(...),
    current_user=Depends(get_authenticated_user),
    ShapesService: ShapesService = Depends(get_service(ShapesService))
):
    shape_update = ShapesService.update_shape(id, name)

    return shape_update


@router.get('/{id}', response_model=ShapeResponse)
def get_shape_by_id(
    id: int,
    current_user=Depends(get_authenticated_user),
    ShapesService: ShapesService = Depends(get_service(ShapesService))
):
    shape = ShapesService.get_by_id(id)

    return shape


@router.post("/{shape_id}/image")
def upload_shape_image(
    shape_id: int,
    image_data: UploadFile = File(...),
    current_user=Depends(get_authenticated_user),
    ShapesService: ShapesService = Depends(get_service(ShapesService))
):
    ShapesService.upload_shape_image(shape_id , image_data)

    return Response(status_code=status.HTTP_200_OK)


@router.delete('/{id}/soft-delete')
def soft_delete_shape(
    id: int,
    current_user=Depends(get_authenticated_user),
    ShapesService: ShapesService = Depends(get_service(ShapesService))
):
    ShapesService.soft_delete_shape(id)

    return Response(status_code=status.HTTP_200_OK)









