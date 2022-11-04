from datetime import datetime
from sqlalchemy import and_
from app.core.service import BaseService
from app.models.fish_original import OriginalFishes
from app.models.fish_type import FishTypes
from app.schemas.fish_original import OriginalFishUpdateRequest, OriginFishCreateRequest
from fastapi import HTTPException, status, Response, UploadFile, File
from app.utils.generate import generate_code
from app.models.image import Images
from app.services.image import ImagesService
from typing import List
from app.utils.file import image_file
from app.core.settings import settings
from app.schemas.image import ImagesType
from app.models.base_season_pond import BaseSeasonPonds

class OriginalFishesService(BaseService):

    def get_by_id(self, id: int):
        original_fish = self.db.query(OriginalFishes).filter(OriginalFishes.id == id).first()

        if not original_fish:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Original fish with id: {id} does not exist",
                            'code': 'ER0027'
                        }]
                )
        return original_fish

    def create(self, fish_data: OriginFishCreateRequest):
        if fish_data.fish_type_id:
            fish_type = self.db.query(FishTypes).filter(and_(FishTypes.id == fish_data.fish_type_id, FishTypes.deleted_at.is_(None))).first()

            if not fish_type:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Loại cá không tồn tại hoặc đã bị xóa",
                            'code': 'ER0028'
                        }]
                )
                
        fish_origin = self.db.query(OriginalFishes).filter(and_(OriginalFishes.name == fish_data.name, OriginalFishes.deleted_at.is_(None))).first()

        if fish_origin:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0029'
                        }]
                )

        max_id = self.db.execute("""
        select max(id) from original_fishes 
        """).first()

        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'CA-'
        if generate < 10:
            code = f'{prefix}{0}{0}{generate}'
        elif generate >= 10 and generate < 100:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_original_fish = OriginalFishes(
            code=code,
            fish_type_id=fish_data.fish_type_id,
            name=fish_data.name,
            description=fish_data.description
        )
        self.db.add(new_original_fish)
        self.db.commit()
        self.db.refresh(new_original_fish)

        return new_original_fish

    def get_all(self):
        original_fishes = self.db.query(OriginalFishes)

        original_fishes = original_fishes.filter(OriginalFishes.deleted_at.is_(None))

        return original_fishes.order_by(OriginalFishes.code).all()

    def update_original_fish(self, id: int, fish_data: OriginalFishUpdateRequest):
        if fish_data.fish_type_id:
            fish_type = self.db.query(FishTypes).filter(and_(FishTypes.id == fish_data.fish_type_id, FishTypes.deleted_at.is_(None))).first()

            if not fish_type:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Loại cá không tồn tại hoặc đã bị xóa",
                            'code': 'ER0028'
                        }]
                )

        original_fish = self.get_by_id(id)
        
        origin_fish_query = self.db.query(OriginalFishes)
        if original_fish.name != fish_data.name:
            origin_fish_exist = origin_fish_query.filter(and_(OriginalFishes.name == fish_data.name, OriginalFishes.deleted_at.is_(None))).first()
            if origin_fish_exist:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0029'
                        }]
                )

        origin_fish_query.filter(OriginalFishes.id == id).update(fish_data.dict())
        self.db.commit()

        return original_fish

    def delete_original(self, id: int):
        self.get_by_id(id)
        original_fish_images = self.db.query(Images) \
            .filter(Images.record_id == id, Images.record_type == type.original_fish_types).all()
        for img in original_fish_images:
            ImagesService.delete_file_s3(img.file_name)
        self.db.query(OriginalFishes).filter(OriginalFishes.id == id).delete(synchronize_session=False)
        self.db.commit()

    def upload_origin_fish_image(self, origin_fish_id: int, image_data: UploadFile = File(...)):
        origin_fish = self.db.query(OriginalFishes).filter(OriginalFishes.id == origin_fish_id).first()

        if not origin_fish:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cá giống không tồn tại.",
            )

        image_tail = image_file(image_data)
        filename = ImagesService.upload_photo_s3(image_data)
        image_url = f'{settings.s3_endpoint}/{filename}'
        record_type = ImagesType.original_fish_types

        ImagesService.upload_image(self, origin_fish_id, record_type, image_tail, filename, image_url)

        self.db.commit()

    
    def upload_multi_origin_fish_image(self, origin_fish_id: int, image_datas: List[UploadFile] = File(...)):
        origin_fish = self.db.query(OriginalFishes).filter(OriginalFishes.id == origin_fish_id).first()

        if not origin_fish:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cá giống không tồn tại.",
            )

        for img in image_datas:
            image_tail = image_file(img)
            filename = ImagesService.upload_photo_s3(img)
            image_url = f'{settings.s3_endpoint}/{filename}'
            record_type = ImagesType.original_fish_types

            ImagesService.upload_image(self, origin_fish_id, record_type, image_tail, filename, image_url)

        self.db.commit()


    def soft_delete_original_fish(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        origin_fish_in_base_seasons = self.db.query(BaseSeasonPonds).filter(and_(BaseSeasonPonds.origin_fish_id == id,  BaseSeasonPonds.status.not_in(['Kết thúc','Đã hủy']))).all()

        if origin_fish_in_base_seasons:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Cá giống hiện tại đang trong vụ nuôi.",
                            'code': 'ER0030'
                        }]
                )
           
        self.db.query(OriginalFishes).filter(OriginalFishes.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()
