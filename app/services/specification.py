from datetime import datetime
from app.core.service import BaseService
from app.models.specification import Specifications
from app.schemas.specification import SpecificationCreateForm, SpecificationFilter
from fastapi import HTTPException, status, UploadFile, File, Depends
from app.utils.file import image_file
from app.core.settings import settings
from app.services.image import ImagesService
from app.schemas.image import ImagesType
from sqlalchemy import desc



class SpecificationsService(BaseService):

    def get_by_id(self, id: int):
        specification = self.db.query(Specifications).filter(Specifications.id == id).first()

        if not specification:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Specification with id: {id} does not exist",
                            'code': 'ER0053'
                        }]
                )
                
        return specification

    def create(self, specification_data: SpecificationCreateForm):
        specifications = self.db.query(Specifications).filter(Specifications.deleted_at.is_(None)).all()

        for i in specifications:
            if  (i.shape_id == specification_data.shape_id and i.unit_id == specification_data.unit_id and i.type == specification_data.type and i.amount == specification_data.amount):
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Qui cách này đã tồn tại",
                            'code': 'ER0054'
                        }]
                )

        max_id = self.db.execute("""
        select max(id) from specifications 
        """).first()

        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'QCHT-'
        if generate < 10:
            code = f'{prefix}{0}{0}{generate}'
        elif generate < 100 and generate >= 10:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_specification = Specifications(
            code=code,
            shape_id=specification_data.shape_id,
            unit_id=specification_data.unit_id,
            amount=specification_data.amount,
            type=specification_data.type
        )
        self.db.add(new_specification)
        self.db.flush()

        if specification_data.image_data:
            image_tail = image_file(specification_data.image_data)
            filename = ImagesService.upload_photo_s3(specification_data.image_data)
            image_url = f'{settings.s3_endpoint}/{filename}'
            record_type = ImagesType.specification_types
            ImagesService.upload_image(self, new_specification.id, record_type, image_tail, filename, image_url)

        self.db.commit()
        self.db.refresh(new_specification)

        return new_specification

    def get_all(self, specification_filter: SpecificationFilter):
        specifications = self.db.query(Specifications)

        if specification_filter.code:
            specifications = specifications.filter(Specifications.code == specification_filter.code)

        if specification_filter.shape_id:
            specifications = specifications.filter(Specifications.shape_id == specification_filter.shape_id)

        if specification_filter.unit_id:
            specifications = specifications.filter(Specifications.unit_id == specification_filter.unit_id)

        if specification_filter.type:
            specifications = specifications.filter(Specifications.type == specification_filter.type)

        specifications = specifications.filter(Specifications.deleted_at.is_(None))

        return specifications.order_by(desc(Specifications.created_at)).all()

    def update_specification(self, id: int, specification_data: SpecificationCreateForm):
        specification = self.get_by_id(id)

        specifications = self.db.query(Specifications).filter(Specifications.deleted_at.is_(None)).all()

        for i in specifications:
            if i.id != id:
                if  (i.shape_id == specification_data.shape_id and i.unit_id == specification_data.unit_id and i.type == specification_data.type and i.amount == specification_data.amount):
                    raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Qui cách này đã tồn tại",
                            'code': 'ER0054'
                        }]
                )

        self.db.query(Specifications).filter(Specifications.id == id).update(specification_data.dict())
        self.db.commit()

        return specification
    

    def upload_specification_image(self, specification_id:int, image_data: UploadFile = File(...)):
        specification = self.db.query(Specifications).filter(Specifications.id == specification_id).first()

        if not specification:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Qui cách này không tồn tại.",
            )

        image_tail = image_file(image_data)
        filename = ImagesService.upload_photo_s3(image_data)
        image_url = f'{settings.s3_endpoint}/{filename}'
        record_type = ImagesType.specification_types

        ImagesService.upload_image(self, specification_id, record_type, image_tail, filename, image_url)

        self.db.commit()


    def soft_delete_specification(self, id: int):
        self.get_by_id(id)        
        current_time = datetime.now()

        self.db.query(Specifications).filter(Specifications.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()

