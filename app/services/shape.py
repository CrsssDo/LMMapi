from datetime import datetime
from sqlalchemy import and_
from app.core.service import BaseService
from app.models.shape import Shapes
from fastapi import HTTPException, status, UploadFile, File
from app.utils.generate import generate_code
from app.models.image import Images
from app.services.image import ImagesService
from typing import List
from app.utils.file import image_file
from app.core.settings import settings
from app.schemas.image import ImagesType


class ShapesService(BaseService):

    def get_by_id(self, id: int):
        shape = self.db.query(Shapes).filter(Shapes.id == id).first()

        if not shape:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Shape with id: {id} does not exist",
                            'code': 'ER0052'
                        }]
                )
            
        return shape

    def create(self, name: str):
        shape = self.db.query(Shapes).filter(and_(Shapes.name == name, Shapes.deleted_at.is_(None))).first()

        if shape:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0052'
                        }]
                )

        max_id = self.db.execute("""
                select max(id) from shapes 
                """).first()
        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'HT-'
        if generate < 10:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_shape = Shapes(
            code=code,
            name=name
            )
        self.db.add(new_shape)
        self.db.commit()
        self.db.refresh(new_shape)

        return new_shape

    def get_all(self):
        shapes = self.db.query(Shapes)

        shapes = shapes.filter(Shapes.deleted_at.is_(None))

        return shapes.order_by(Shapes.code).all()

    def update_shape(self, id: int, name: str):
        shape = self.get_by_id(id)
        shape_query = self.db.query(Shapes)
        if shape.name != name:
            shape_exist = shape_query.filter(and_(Shapes.name == name, Shapes.deleted_at.is_(None))).first()
            if shape_exist:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0052'
                        }]
                )

        shape_query.filter(Shapes.id == id).update({"name": name}, synchronize_session=False)
        self.db.commit()

        return shape
        
    def upload_shape_image(self, shape_id: int, image_data: UploadFile = File(...)):
        shape = self.db.query(Shapes).filter(Shapes.id == shape_id).first()

        if not shape:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Hình thức không tồn tại.",
            )

        image_tail = image_file(image_data)
        filename = ImagesService.upload_photo_s3(image_data)
        image_url = f'{settings.s3_endpoint}/{filename}'
        record_type = ImagesType.shape_types

        ImagesService.upload_image(self, shape_id, record_type, image_tail, filename, image_url)

        self.db.commit()

    def soft_delete_shape(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        self.db.query(Shapes).filter(Shapes.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()

    


