from datetime import datetime
from app.core.service import BaseService
from app.schemas.disease import DiseaseCreateRequest, DiseaseUpdateRequest
from app.models.disease import Diseases
from fastapi import HTTPException, status, UploadFile, File, Response
from typing import List
from app.utils.file import image_file
from app.models.image import Images
from app.services.image import ImagesService
from app.core.settings import settings
from app.models.disease import Diseases
from app.schemas.image import ImagesType
from sqlalchemy import and_


class DiseasesService(BaseService):

    def get_by_id(self, id: int):
        disease = self.db.query(Diseases).filter(Diseases.id == id).first()

        if not disease:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Disease with id: {id} does not exist",
                            'code': 'ER0021'
                        }]
                )

        return disease

    def create(self, disease_data: DiseaseCreateRequest):
        disease = self.db.query(Diseases).filter(and_(Diseases.name == disease_data.name, Diseases.deleted_at.is_(None))).first()

        if disease:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0022'
                        }]
                )
        
        max_id = self.db.execute("""
        select max(id) from diseases 
        """).first()

        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'BCA-'
        if generate < 10:
            code = f'{prefix}{0}{0}{generate}'
        elif generate >= 10 and generate < 100:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_disease = Diseases(
            code=code,
            name=disease_data.name,
            description=disease_data.description
        )
        self.db.add(new_disease)
        self.db.commit()
        self.db.refresh(new_disease)

        return new_disease

    def get_all(self):
        diseases = self.db.query(Diseases)

        diseases = diseases.filter(Diseases.deleted_at.is_(None))

        return diseases.order_by(Diseases.name).all()

    def update_fish_diseases(self, id: int, disease_data: DiseaseUpdateRequest):
        disease = self.get_by_id(id)

        disease_query = self.db.query(Diseases)
        if disease.name != disease_data.name:
            disease_exist = disease_query.filter(and_(Diseases.name == disease_data.name, Diseases.deleted_at.is_(None))).first()
            if disease_exist:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0022'
                        }]
                )
                        
        self.db.query(Diseases).filter(Diseases.id == id).update(disease_data.dict())
        self.db.commit()

        return disease

    def delete_disease(self, id: int):
        self.get_by_id(id)
        fish_disease_images = self.db.query(Images)\
            .filter(Images.record_id == id, Images.record_type == type.fish_disease_types).all()
        for img in fish_disease_images:
            ImagesService.delete_file_s3(img.file_name)
        self.db.query(Diseases).filter(Diseases.id == id).delete(synchronize_session=False)
        self.db.commit()

    def upload_disease_image(self, disease_id:int, image_data: UploadFile = File(...)):
        disease = self.db.query(Diseases).filter(Diseases.id == disease_id).first()

        if not disease:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Bệnh của cá không tồn tại.",
                            'code': 'ER0023'
                        }]
                )
    
        image_tail = image_file(image_data)
        filename = ImagesService.upload_photo_s3(image_data)
        image_url = f'{settings.s3_endpoint}/{filename}'
        record_type = ImagesType.fish_disease_types

        ImagesService.upload_image(self, disease_id, record_type, image_tail, filename, image_url)

        self.db.commit()

    
    def upload_multi_disease_image(self, disease_id: int, image_datas: List[UploadFile] = File(...)):
        disease = self.db.query(Diseases).filter(Diseases.id == disease_id).first()

        if not disease:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Bệnh của cá không tồn tại.",
                            'code': 'ER0023'
                        }]
                )

        for img in image_datas:
            image_tail = image_file(img)
            filename = ImagesService.upload_photo_s3(img)
            image_url = f'{settings.s3_endpoint}/{filename}'
            record_type = ImagesType.fish_disease_types

            ImagesService.upload_image(self, disease_id, record_type, image_tail, filename, image_url)

        self.db.commit()

    def soft_delete_disease(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        self.db.query(Diseases).filter(Diseases.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()

