from datetime import datetime
from sqlalchemy import and_
from app.core.service import BaseService
from app.models.chemistry import Chemistries
from ..models.supplier import Suppliers
from app.schemas.chemistry import ChemistryCreateRequest, ChemistryUpdateRequest, ChemistryStatusUpdateRequest
from fastapi import HTTPException, Query, status, UploadFile, File, Response
from app.utils.generate import generate_code
from app.models.image import Images
from app.services.image import ImagesService
from typing import List, Optional
from app.utils.file import image_file
from app.core.settings import settings
from app.schemas.image import ImagesType, ChemistryImageSubType
from app.models.chemistry_in import ChemistryIns
from app.models.chemistry_type import ChemistryTypes


class ChemistriesService(BaseService):

    def get_by_id(self, id: int):
        chemistry = self.db.query(Chemistries).filter(Chemistries.id == id).first()

        if not chemistry:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Chemistry with id: {id} does not exist",
                            'code': 'ER0013'
                        }]
                )
                
        return chemistry

    def create(self, chemistry_data: ChemistryCreateRequest):
        max_id = self.db.execute("""
                select max(id) from chemistries 
                """).first()
        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'HC-'
        if generate < 10:
            code = f'{prefix}{0}{0}{0}{generate}'
        elif generate >= 10 and generate < 100:
            code = f'{prefix}{0}{0}{generate}'
        elif generate >=100 and generate < 1000:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_chemistry = Chemistries(
            code=code,
            receiver_code=chemistry_data.receiver_code,
            name=chemistry_data.name,
            uses=chemistry_data.uses,
            element=chemistry_data.element,
            instructions_for_use=chemistry_data.instructions_for_use,
            supplier_id=chemistry_data.supplier_id,
            status=chemistry_data.status,
            chemistry_type_id=chemistry_data.chemistry_type_id,
            analysed_date=chemistry_data.analysed_date,
            declared_date=chemistry_data.declared_date
        )
        self.db.add(new_chemistry)
        self.db.commit()
        self.db.refresh(new_chemistry)

        return new_chemistry

    def get_all(self, status: bool = Query(False)):
        chemistry = self.db.query(Chemistries)

        if status == True:
            chemistry = chemistry.filter(Chemistries.status == status)

        chemistry = chemistry.filter(Chemistries.deleted_at.is_(None))

        return chemistry.order_by(Chemistries.code).all()

    def update_chemistry(self, id: int, chemistries_data: ChemistryUpdateRequest):
        chemistry = self.get_by_id(id)

        if chemistries_data.chemistry_type_id:
            type_deleted = self.db.query(ChemistryTypes).filter(ChemistryTypes.id == chemistries_data.chemistry_type_id)\
                            .filter(ChemistryTypes.deleted_at.is_not(None)).first()

            if type_deleted:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu loại hóa chất {type_deleted.code}{' '}{type_deleted.name} đã bị xóa.",
                            'code': 'ER0014'
                        }]
                )

        if chemistries_data.supplier_id:
            supplier_deleted = self.db.query(Suppliers).filter(Suppliers.id == chemistries_data.supplier_id)\
                            .filter(Suppliers.deleted_at.is_not(None)).first()

            if supplier_deleted:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu nhà cung cấp {supplier_deleted.supplier_code}{' '}{supplier_deleted.name} đã bị xóa.",
                            'code': 'ER0015'
                        }]
                )

        self.db.query(Chemistries).filter(Chemistries.id == id).update(chemistries_data.dict())
        self.db.commit()

        return chemistry

    def update_status(self, id: int, chemistry_status: ChemistryStatusUpdateRequest):
        chemistry = self.get_by_id(id)
        self.db.query(Chemistries).filter(Chemistries.id == id).update(chemistry_status.dict())
        self.db.commit()

        return chemistry

    def upload_chemistry_image(self, chemistry_id:int, image_data: UploadFile = File(...), chemistry_subtype: ChemistryImageSubType = None):
        chemistry = self.db.query(Chemistries).filter(Chemistries.id == chemistry_id).first()

        if not chemistry:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Hóa chất không tồn tại.",
            )

        image_tail = image_file(image_data)
        filename = ImagesService.upload_photo_s3(image_data)
        image_url = f'{settings.s3_endpoint}/{filename}'
        record_type = ImagesType.chemistry_types

        ImagesService.upload_image(self, chemistry_id, record_type, image_tail, filename, image_url, chemistry_subtype)

        self.db.commit()

    
    def upload_multi_chemistry_image(self, chemistry_id :int, image_datas: List[UploadFile] = File(...), chemistry_subtypes: ChemistryImageSubType = None):
        chemistry = self.db.query(Chemistries).filter(Chemistries.id == chemistry_id).first()

        if not chemistry:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Hóa chất không tồn tại.",
            )

        for img in image_datas:
            image_tail = image_file(img)
            filename = ImagesService.upload_photo_s3(img)
            image_url = f'{settings.s3_endpoint}/{filename}'
            record_type = ImagesType.chemistry_types

            ImagesService.upload_image(self, chemistry_id, record_type, image_tail, filename, image_url, chemistry_subtypes)

        self.db.commit()

    def soft_delete_chemistry(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        chemistry_in = self.db.query(ChemistryIns).filter(and_(ChemistryIns.chemistry_id == id, ChemistryIns.inventory > 0)).all()

        if chemistry_in:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Hóa chất vẫn còn trong kho.",
                            'code': 'ER0016'
                        }]
                )

        self.db.query(Chemistries).filter(Chemistries.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()