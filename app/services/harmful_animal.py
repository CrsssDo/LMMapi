from datetime import datetime
from app.core.service import BaseService
from app.models.harmful_animal import HarmfulAnimals
from app.schemas.harmful_animal import HarmfulAnimalCreateRequest
from fastapi import HTTPException, status, Response, UploadFile, File
from app.models.image import Images
from app.services.image import ImagesService
from typing import List
from app.utils.file import image_file
from app.core.settings import settings
from app.schemas.image import ImagesType
from sqlalchemy import and_

class HarmfulAnimalsService(BaseService):

    def get_by_id(self, id: int):
        harmful_animal = self.db.query(HarmfulAnimals).filter(HarmfulAnimals.id == id).first()

        if not harmful_animal:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Animal with id: {id} does not exist",
                            'code': 'ER0037'
                        }]
                )

        return harmful_animal

    def create(self, animal_data: HarmfulAnimalCreateRequest):
        harmful_animal = self.db.query(HarmfulAnimals).filter(and_(HarmfulAnimals.name == animal_data.name, HarmfulAnimals.deleted_at.is_(None))).first()

        if harmful_animal:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0038'
                        }]
                )

        max_id = self.db.execute("""
        select max(id) from harmful_animals 
        """).first()

        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'DVGH-'
        if generate < 10:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_animal = HarmfulAnimals(
            code=code,
            name=animal_data.name

        )
        self.db.add(new_animal)
        self.db.commit()
        self.db.refresh(new_animal)

        return new_animal

    def get_all(self):
        harmful_animals = self.db.query(HarmfulAnimals)

        harmful_animals = harmful_animals.filter(HarmfulAnimals.deleted_at.is_(None))

        return harmful_animals.order_by(HarmfulAnimals.name).all()

    def update_harmful_animal(self, id: int,animal_data: HarmfulAnimalCreateRequest):
        harmful_animal = self.get_by_id(id)

        harmful_animal_query = self.db.query(HarmfulAnimals)
        if harmful_animal.name != animal_data.name:
            harmful_animal_exist = harmful_animal_query.filter(and_(HarmfulAnimals.name == animal_data.name, HarmfulAnimals.deleted_at.is_(None))).first()
            if harmful_animal_exist:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0038'
                        }]
                )
            
        self.db.query(HarmfulAnimals).filter(HarmfulAnimals.id == id).update(animal_data.dict())
        self.db.commit()

        return harmful_animal

    def delete_harmful_animal(self, id: int):
        self.get_by_id(id)
        animal_images = self.db.query(Images) \
            .filter(Images.record_id == id, Images.record_type == type.harmful_animal_types).all()
        for img in animal_images:
            ImagesService.delete_file_s3(img.file_name)
        self.db.query(HarmfulAnimals).filter(HarmfulAnimals.id == id).delete(synchronize_session=False)
        self.db.commit()

    def upload_animal_image(self, animal_id: int, image_data: UploadFile = File(...)):
        animal = self.db.query(HarmfulAnimals).filter(HarmfulAnimals.id == animal_id).first()

        if not animal:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Động vật gây hại không tồn tại.",
            )

        image_tail = image_file(image_data)
        filename = ImagesService.upload_photo_s3(image_data)
        image_url = f'{settings.s3_endpoint}/{filename}'
        record_type = ImagesType.harmful_animal_types

        ImagesService.upload_image(self, animal_id, record_type, image_tail, filename, image_url)

        self.db.commit()

    
    def upload_multi_animal_image(self, animal_id: int, image_datas: List[UploadFile] = File(...)):
        animal = self.db.query(HarmfulAnimals).filter(HarmfulAnimals.id == animal_id).first()

        if not animal:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Động vật gây hại không tồn tại.",
            )

        for img in image_datas:
            image_tail = image_file(img)
            filename = ImagesService.upload_photo_s3(img)
            image_url = f'{settings.s3_endpoint}/{filename}'
            record_type = ImagesType.harmful_animal_types

            ImagesService.upload_image(self, animal_id, record_type, image_tail, filename, image_url)

        self.db.commit()


    def soft_delete_animal(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        self.db.query(HarmfulAnimals).filter(HarmfulAnimals.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()


    
