from datetime import datetime
from app.core.service import BaseService
from app.models.equipment import Equipments
from app.schemas.equipment import  EquipmentCreateRequest, EquipmentUpdateRequest
from fastapi import HTTPException, status, UploadFile, File
from app.utils.generate import generate_code
from app.models.image import Images
from app.services.image import ImagesService
from typing import List
from app.utils.file import image_file
from app.core.settings import settings
from app.schemas.image import ImagesType
from sqlalchemy import and_


class EquipmentsService(BaseService):

    def get_by_id(self, id: int):
        equipment = self.db.query(Equipments).filter(Equipments.id == id).first()

        if not equipment:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Equip with id: {id} does not exist",
                            'code': 'ER0025'
                        }]
                )

        return equipment

    def create(self, equipment_data: EquipmentCreateRequest):
        equipment = self.db.query(Equipments).filter(and_(Equipments.name == equipment_data.name, Equipments.deleted_at.is_(None))).first()

        if equipment:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0026'
                        }]
                )
        
        code = equipment_data.code

        max_id = self.db.execute("""
                select max(id) from equipments 
                """).first()
        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        if not code:
            prefix = 'TB-'
            if generate < 10:
                code = f'{prefix}{0}{0}{0}{generate}'
            elif generate >= 10 and generate < 100:
                code = f'{prefix}{0}{0}{generate}'
            else:
                code = f'{prefix}{0}{generate}'

        new_equipment = Equipments(
            code=code,
            name=equipment_data.name,
            description=equipment_data.description
        )
        self.db.add(new_equipment)
        self.db.commit()
        self.db.refresh(new_equipment)

        return new_equipment

    def get_all(self):
        equipments = self.db.query(Equipments)

        equipments = equipments.filter(Equipments.deleted_at.is_(None))

        return equipments.order_by(Equipments.code).all()

    def update_equipment(self, id: int, equipment_data: EquipmentUpdateRequest):
        equipment = self.get_by_id(id)

        equipment_query = self.db.query(Equipments)
        if equipment.name != equipment_data.name:
            equipment_exist = equipment_query.filter(and_(Equipments.name == equipment_data.name, Equipments.deleted_at.is_(None))).first()
            if equipment_exist:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0026'
                        }]
                )
                
        self.db.query(Equipments).filter(Equipments.id == id).update(equipment_data.dict())
        self.db.commit()

        return equipment

    def delete_equipment(self, id: int):
        self.get_by_id(id)
        equipment_images = self.db.query(Images) \
            .filter(Images.record_id == id, Images.record_type == type.equipment_types).all()
        for img in equipment_images:
            ImagesService.delete_file_s3(img.file_name)
        self.db.query(Equipments).filter(Equipments.id == id).delete(synchronize_session=False)
        self.db.commit()
        
    def upload_equipment_image(self, equipment_id: int, image_data: UploadFile = File(...)):
        equipment = self.db.query(Equipments).filter(Equipments.id == equipment_id).first()

        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Thiết bị không tồn tại.",
            )

        image_tail = image_file(image_data)
        filename = ImagesService.upload_photo_s3(image_data)
        image_url = f'{settings.s3_endpoint}/{filename}'
        record_type = ImagesType.equipment_types

        ImagesService.upload_image(self, equipment_id, record_type, image_tail, filename, image_url)

        self.db.commit()

    
    def upload_multi_equipment_image(self, equipment_id: int, image_datas: List[UploadFile] = File(...)):
        equipment = self.db.query(Equipments).filter(Equipments.id == equipment_id).first()

        if not equipment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Thiết bị không tồn tại.",
            )

        for img in image_datas:
            image_tail = image_file(img)
            filename = ImagesService.upload_photo_s3(img)
            image_url = f'{settings.s3_endpoint}/{filename}'
            record_type = ImagesType.equipment_types

            ImagesService.upload_image(self, equipment_id, record_type, image_tail, filename, image_url)

        self.db.commit()


    def soft_delete_equipment(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        self.db.query(Equipments).filter(Equipments.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()








