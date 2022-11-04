from datetime import datetime
from pickletools import OpcodeInfo
from sqlalchemy import desc, or_, and_, text
from app.core.service import BaseService
from app.models.pond import Ponds, PondCategorizes, PondTypes
from app.schemas.pond import  PondCreateRequest, PondUpdateRequest, PondStatusUpdateRequest, PondTypeCreateRquest
from fastapi import HTTPException, status, UploadFile, File
from app.utils.file import image_file
from typing import List, Optional
from app.core.settings import settings
from app.services.image import ImagesService
from app.models.image import Images
from app.schemas.image import ImagesType
from app.models.base_season_pond import BaseSeasonPonds
from app.models.fish_original import OriginalFishes


class PondsService(BaseService):

    def get_by_id(self, id: int):
        pond = self.db.query(Ponds).filter(Ponds.id == id).first()
        if not pond:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Pond with id: {id} does not exist",
                            'code': 'ER0047'
                        }]
                )
        return pond

    def create(self, pond_data: PondCreateRequest):
        if pond_data.number_order:
            pond_numer_order = self.db.query(Ponds).filter(Ponds.number_order == pond_data.number_order)\
                                                    .filter(Ponds.adopt_area_id == pond_data.adopt_area_id)\
                                                    .filter(Ponds.pond_type_id == pond_data.pond_type_id).first()
            if pond_numer_order:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    [{
                            'error' : True,
                            'message': f"Mã số đã được sử dụng cho Ao/Bể {pond_numer_order.code}",
                            'code': 'ER0048'
                        }]
                )

        if pond_data.pond_type_id:
            pond_type = self.db.query(PondTypes).filter(PondTypes.id == pond_data.pond_type_id).first()

            pond_map_name = f'{pond_type.symbol}'


        max_id = self.db.execute("""
        select max(id) from ponds 
        """).first()

        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'AB-'

        if generate < 10:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_pond = Ponds(
            code=code, 
            pond_map_name=pond_map_name,
            area=pond_data.area,
            volume=pond_data.volume,
            location=pond_data.location,
            number_order=pond_data.number_order,
            adopt_area_id=pond_data.adopt_area_id,
            pond_type_id=pond_data.pond_type_id,
            pond_categorize_id=pond_data.pond_categorize_id,
            finished_date=pond_data.finished_date,
            status=pond_data.status
        )
        self.db.add(new_pond)
        self.db.commit()
        self.db.refresh(new_pond)

        return new_pond

    def get_all(self, adopt_id: Optional[int] = None, pond_status: Optional[bool] =  False, pond_in_base_season: Optional[bool] = False, base_season: Optional[bool] = False):
        ponds = self.db.query(Ponds)

        if adopt_id:
            ponds = ponds.filter(Ponds.adopt_area_id == adopt_id)

        if pond_in_base_season:
            ponds = ponds.join(BaseSeasonPonds.pond).filter(BaseSeasonPonds.status.not_in(['Chờ nuôi','Đã hủy','Kết thúc']))

        if pond_status == True:
            ponds = ponds.filter(Ponds.status == pond_status)

        if base_season == True:
            sub_query = ~self.db.query(BaseSeasonPonds).filter(BaseSeasonPonds.pond_id == Ponds.id, BaseSeasonPonds.status.not_in(['Kết thúc','Đã hủy'])).exists()

            ponds = ponds.filter(sub_query)

        ponds = ponds.filter(Ponds.deleted_at.is_(None))
            
        ponds = ponds.order_by(Ponds.pond_map_name, Ponds.number_order).all()

        pond_can_rate = self.db.query(Ponds.id)
        sub_query = self.db.query(BaseSeasonPonds).filter(BaseSeasonPonds.pond_id == Ponds.id, BaseSeasonPonds.status.in_(['Đang nuôi','Đang thu hoạch','Đã thu hoạch','Đang vệ sinh','Đã vệ sinh','Đang kiểm tra','Đã kiểm tra'])).exists()

        pond_can_rate = pond_can_rate.filter(sub_query).all()

        base_seasons = self.db.query(BaseSeasonPonds).join(Ponds, BaseSeasonPonds.pond_id == Ponds.id).order_by(BaseSeasonPonds.id).all()

        for i in base_seasons:
            for j in ponds:
                if i.pond_id == j.id:
                    j.base_season_id = i.id
                    j.base_season_status = i.status

        for i in pond_can_rate:
            for j in ponds:
                if i.id == j.id:
                    j.can_rate = True

        return ponds


    def get_pond_by_fish_type(self, adopt_id: int, fish_type_id: int):
        ponds = self.db.query(Ponds).join(BaseSeasonPonds, BaseSeasonPonds.pond_id == Ponds.id).join(OriginalFishes, OriginalFishes.id == BaseSeasonPonds.origin_fish_id)\
                                    .filter(Ponds.adopt_area_id == adopt_id)\
                                    .filter(Ponds.status == True)\
                                    .filter(BaseSeasonPonds.status.not_in(['Kết thúc','Đã hủy']))\
                                    .filter(OriginalFishes.fish_type_id == fish_type_id)
                                
        return ponds.all()


    def get_numer_order_by_pond_type(self, pond_type_id: int, adopt_id: int, pond_id: Optional[int] = None):
        pond_has_number_order = self.db.query(Ponds).filter(Ponds.pond_type_id == pond_type_id)\
                                                    .filter(Ponds.adopt_area_id == adopt_id)\
                                                    .filter(Ponds.number_order.is_not(None)).all()
        pond = None
        if pond_id:
            pond = self.get_by_id(pond_id)

        selected_number_order = []
        for i in pond_has_number_order:
            if not pond:
                selected_number_order.append(i.number_order)
            else:
                if (pond.number_order != i.number_order):
                    selected_number_order.append(i.number_order)

        return selected_number_order


    def update_pond(self, id: int, pond_data: PondUpdateRequest):
        pond = self.get_by_id(id)

        if pond_data.number_order:
            pond_numer_order = self.db.query(Ponds).filter(Ponds.number_order == pond_data.number_order)\
                                                    .filter(Ponds.adopt_area_id == pond_data.adopt_area_id)\
                                                    .filter(Ponds.pond_type_id == pond_data.pond_type_id).first()
            if pond_numer_order:
                if pond.id != pond_numer_order.id:
                    raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    [{
                            'error' : True,
                            'message': f"Mã số đã được sử dụng cho Ao/Bể {pond_numer_order.code}",
                            'code': 'ER0048'
                        }]
                )

        if pond_data.pond_type_id:
            pond_type = self.db.query(PondTypes).filter(and_(PondTypes.id == pond_data.pond_type_id, PondTypes.deleted_at.is_(None))).first()

            if not pond_type:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Dữ liệu loại ao/bể {pond_type.code}{' '}{pond_type.name} đã bị xóa."
                )

            pond_map_name = f'{pond_type.symbol}'

            self.db.query(Ponds).filter(Ponds.id == id).update({"pond_map_name": pond_map_name}, synchronize_session=False)
            
                
        self.db.query(Ponds).filter(Ponds.id == id).update(pond_data.dict())
        self.db.commit()

        return pond

    def update_status(self, id: int, pond_status: PondStatusUpdateRequest):
        pond = self.get_by_id(id)
        self.db.query(Ponds).filter(Ponds.id == id).update(pond_status.dict())
        self.db.commit()

        return pond

    def delete_pond(self, id: int):
        self.get_by_id(id)
        pond_images = self.db.query(Images)\
            .filter(Images.record_id == id, Images.record_type == type.pond_types).all()
        for img in pond_images:
            ImagesService.delete_file_s3(img.file_name)
        self.db.query(Ponds).filter(Ponds.id == id).delete(synchronize_session=False)
        self.db.commit()

    def upload_pond_image(self, pond_id:int, image_data: UploadFile = File(...)):
        pond = self.db.query(Ponds).filter(Ponds.id == pond_id).first()

        if not pond:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Bể không tồn tại.",
            )

        image_tail = image_file(image_data)
        filename = ImagesService.upload_photo_s3(image_data)
        image_url = f'{settings.s3_endpoint}/{filename}'
        record_type = ImagesType.pond_types

        ImagesService.upload_image(self, pond_id, record_type, image_tail, filename, image_url)

        self.db.commit()

    
    def upload_multi_pond_image(self, pond_id:int, image_datas: List[UploadFile] = File(...)):
        pond = self.db.query(Ponds).filter(Ponds.id == pond_id).first()

        if not pond:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Bể không tồn tại.",
            )

        for img in image_datas:
            image_tail = image_file(img)
            filename = ImagesService.upload_photo_s3(img)
            image_url = f'{settings.s3_endpoint}/{filename}'
            record_type = ImagesType.pond_types

            ImagesService.upload_image(self, pond_id, record_type, image_tail, filename, image_url)

        self.db.commit()


class PondTypesService(BaseService):

    def get_by_id(self, id:int):
        pond_type = self.db.query(PondTypes).filter(PondTypes.id == id).first()

        if not pond_type:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"pond type with id: {id} does not exist")
        return pond_type

    def get_all(self):
        pond_types = self.db.query(PondTypes)

        pond_types = pond_types.filter(PondTypes.deleted_at.is_(None))

        return pond_types.order_by(PondTypes.name).all()

    def create(self, pond_type_data: PondTypeCreateRquest):
        pond_type_exist = self.db.query(PondTypes).filter(and_(PondTypes.name == pond_type_data.name, PondTypes.deleted_at.is_(None))).first()

        if pond_type_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loại ao/bể đã tồn tại"
            )

        max_id = self.db.execute("""
        select max(id) from pond_types 
        """).first()

        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'LAB-'

        if generate < 10:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'
        
        new_pond_type = PondTypes(
            code=code, 
            name=pond_type_data.name,
            symbol=pond_type_data.symbol
        )
        self.db.add(new_pond_type)
        self.db.commit()
        self.db.refresh(new_pond_type)

        return new_pond_type

    def update_pond_type(self, id:int, pond_type_data: PondTypeCreateRquest):
        pond_type = self.get_by_id(id)
        if pond_type_data.name:
            pond_type_exist = self.db.query(PondTypes).filter(and_(PondTypes.name == pond_type_data.name, PondTypes.deleted_at.is_(None))).first()
            if pond_type_exist:
                if pond_type.id != pond_type_exist.id:
                    raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Dữ liệu loại ao/bể đã tồn tại",
                    )
            self.db.query(PondTypes).filter(PondTypes.id == id).update({"name": pond_type_data.name}, synchronize_session=False)

        if pond_type_data.symbol:
            self.db.query(PondTypes).filter(PondTypes.id == id).update({"symbol": pond_type_data.symbol}, synchronize_session=False)

        self.db.commit()

        return pond_type

    def soft_delete_pond_type(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        self.db.query(PondTypes).filter(PondTypes.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()

class PondCategorizesService(BaseService):

    def get_all(self):
        pond_categorizes = self.db.query(PondCategorizes).all()
        return pond_categorizes


