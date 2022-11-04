from datetime import datetime
from sqlalchemy import and_
from app.core.service import BaseService
from app.models.medicine import Medicines
from app.schemas.medicine import MedicineCreateRequest, MedicineUpdateRequest, MedicineStatusUpdateRequest
from fastapi import HTTPException, Query, status, UploadFile, File, Response
from app.utils.generate import generate_code
from app.models.image import Images
from app.services.image import ImagesService
from typing import List, Optional
from app.utils.file import image_file
from app.core.settings import settings
from app.schemas.image import ImagesType, MedicineImageSubType
from app.models.specification import Specifications
from sqlalchemy import and_
from app.models.medicine_in import MedicineIn
from app.models.supplier import Suppliers
from app.models.medicine_type import MedicineTypes


class MedicinesService(BaseService):

    def get_by_id(self, id: int):
        medicine = self.db.query(Medicines).filter(Medicines.id == id).first()

        if not medicine:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Medicine with id: {id} does not exist",
                            'code': 'ER0045'
                        }]
                )
        return medicine

    def create(self, medicine_data: MedicineCreateRequest):
        max_id = self.db.execute("""
                select max(id) from medicines 
                """).first()
        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'TH-'
        if generate < 10:
            code = f'{prefix}{0}{0}{0}{generate}'
        elif generate >=10 and generate < 100:
            code = f'{prefix}{0}{0}{generate}'
        elif generate >= 100 and generate < 1000:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_medicine = Medicines(
            code=code,
            receiver_code=medicine_data.receiver_code,
            name=medicine_data.name,
            uses=medicine_data.uses,
            element=medicine_data.element,
            instructions_for_use=medicine_data.instructions_for_use,
            supplier_id=medicine_data.supplier_id,
            status=medicine_data.status,
            medicine_type_id=medicine_data.medicine_type_id,
            analysed_date=medicine_data.analysed_date,
            declared_date=medicine_data.declared_date
        )
        self.db.add(new_medicine)
        self.db.commit()
        self.db.refresh(new_medicine)

        return new_medicine

    def get_all(self, status: bool = Query(False)):
        medicines = self.db.query(Medicines)

        if status == True:
            medicines = medicines.filter(Medicines.status == status)

        medicines = medicines.filter(Medicines.deleted_at.is_(None))


        return medicines.order_by(Medicines.code).all()

    def update_medicine(self, id: int, medicine_data: MedicineUpdateRequest):
        medicine = self.get_by_id(id)

        if medicine_data.medicine_type_id:
            type_deleted = self.db.query(MedicineTypes).filter(MedicineTypes.id == medicine_data.medicine_type_id)\
                            .filter(MedicineTypes.deleted_at.is_not(None)).first()

            if type_deleted:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Dữ liệu loại thuốc {type_deleted.code}{' '}{type_deleted.name} đã bị xóa.",
            )


        if medicine_data.supplier_id:
            supplier_deleted = self.db.query(Suppliers).filter(Suppliers.id == medicine_data.supplier_id)\
                            .filter(Suppliers.deleted_at.is_not(None)).first()

            if supplier_deleted:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Dữ liệu nhà cung cấp {supplier_deleted.supplier_code}{' '}{supplier_deleted.name} đã bị xóa.",
            )

        self.db.query(Medicines).filter(Medicines.id == id).update(medicine_data.dict())
        self.db.commit()

        return medicine

    def update_status(self, id: int, medicine_status: MedicineStatusUpdateRequest):
        medicine = self.get_by_id(id)
        self.db.query(Medicines).filter(Medicines.id == id).update(medicine_status.dict())
        self.db.commit()

        return medicine

    def delete_medicine(self, id: int):
        self.get_by_id(id)
        medicine_medias = self.db.query(Images) \
            .filter(Images.record_id == id, Images.record_type == type.medicine_types).all()
        for img in medicine_medias:
            ImagesService.delete_file_s3(img.file_name)
        self.db.query(Medicines).filter(Medicines.id == id).delete(synchronize_session=False)
        self.db.commit()

    def upload_medicine_image(self, medicine_id:int, image_data: UploadFile = File(...), medicine_subtype: MedicineImageSubType = None):
        medicine = self.db.query(Medicines).filter(Medicines.id == medicine_id).first()

        if not medicine:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Thuốc không tồn tại.",
            )

        image_tail = image_file(image_data)
        filename = ImagesService.upload_photo_s3(image_data)
        image_url = f'{settings.s3_endpoint}/{filename}'
        record_type = ImagesType.medicine_types

        ImagesService.upload_image(self, medicine_id, record_type, image_tail, filename, image_url, medicine_subtype)

        self.db.commit()

    
    def upload_multi_medicine_image(self, medicine_id:int, image_datas: List[UploadFile] = File(...), medicine_subtype: MedicineImageSubType = None):
        medicine = self.db.query(Medicines).filter(Medicines.id == medicine_id).first()

        if not medicine:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Thuốc không tồn tại.",
            )

        for img in image_datas:
            image_tail = image_file(img)
            filename = ImagesService.upload_photo_s3(img)
            image_url = f'{settings.s3_endpoint}/{filename}'
            record_type = ImagesType.medicine_types

            ImagesService.upload_image(self, medicine_id, record_type, image_tail, filename, image_url, medicine_subtype)

        self.db.commit()


    def soft_delete_medicine(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        medicine_in = self.db.query(MedicineIn).filter(and_(MedicineIn.medicine_id == id, MedicineIn.inventory > 0)).all()

        if medicine_in:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Thuốc vẫn còn trong kho.",
                            'code': 'ER0046'
                        }]
                )

        self.db.query(Medicines).filter(Medicines.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()

