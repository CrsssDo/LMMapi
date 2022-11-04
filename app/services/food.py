from datetime import datetime
from sys import float_repr_style
from sqlalchemy import and_
from app.core.service import BaseService
from app.models.food import Foods
from app.schemas.food import FoodCreateRequest, FoodUpdateRequest, FoodStatusUpdateRequest
from fastapi import HTTPException, status, UploadFile, File, Response
from typing import List
from app.utils.file import image_file
from app.models.image import Images
from app.services.image import ImagesService
from app.core.settings import settings
from app.schemas.image import ImagesType, FoodImageSubType
from app.models.food_in import FoodIn
from app.models.supplier import Suppliers
from app.models.food_type import FoodTypes
from app.models.fish_type import FishTypes
from app.models.base_season_pond import BaseSeasonPonds
from app.models.fish_original import OriginalFishes

class FoodsService(BaseService):

    def get_by_id(self, id: int):
        food = self.db.query(Foods).filter(Foods.id == id).first()

        if not food:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Fish's food with id: {id} does not exist",
                            'code': 'ER0037'
                        }]
                )

        return food

    def create(self, food_data: FoodCreateRequest):
        if food_data.protein_value:
            if food_data.protein_value < 0:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Giá trị độ đạm phải là số nguyên dương",
                            'code': 'ER0038'
                        }]
                )

        if food_data.supplier_id:
            supplier = self.db.query(Suppliers).filter(Suppliers.id == food_data.supplier_id).first()

            if not supplier:
                raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=f"Nhà cung cấp không tồn tại"
                    )

        if food_data.fish_type_id:
            fish_type = self.db.query(FishTypes).filter(and_(FishTypes.id == food_data.fish_type_id, FishTypes.deleted_at.is_(None))).first()

            if not fish_type:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Loại cá không tồn tại hoặc đã bị xóa",
            )

        max_id = self.db.execute("""
                select max(id) from foods 
                """).first()
        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'TA-'
        if generate < 10:
            code = f'{prefix}{0}{0}{0}{generate}'
        elif generate >=10 and generate < 100:
            code = f'{prefix}{0}{0}{generate}'
        elif generate >= 100 and generate < 1000:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_food = Foods(
            code=code,
            name=food_data.name,
            type=food_data.type,
            receiver_code=food_data.receiver_code,
            uses=food_data.uses,
            element=food_data.element,
            instructions_for_use=food_data.instructions_for_use,
            supplier_id=food_data.supplier_id,
            food_type_id=food_data.food_type_id,
            fish_type_id=food_data.fish_type_id,
            protein_value=food_data.protein_value,
            status=food_data.status,
            analysed_date=food_data.analysed_date,
            declared_date=food_data.declared_date
        )
        self.db.add(new_food)
        self.db.commit()
        self.db.refresh(new_food)

        return new_food

    def get_all(self, pond_id: int = None):
        foods = self.db.query(Foods)
        if pond_id:
            pond_in_base_season = self.db.query(BaseSeasonPonds).filter(and_(BaseSeasonPonds.pond_id == pond_id, BaseSeasonPonds.status.not_in(['Kết thúc','Đã hủy']))).first()

            fish = self.db.query(OriginalFishes).filter(OriginalFishes.id == pond_in_base_season.origin_fish_id).first()

            foods = foods.filter(Foods.fish_type_id == fish.fish_type_id)

        foods = foods.filter(Foods.deleted_at.is_(None))

        return foods.order_by(Foods.code).all()

    def update_fish_food(self, id: int, food_data: FoodUpdateRequest):
        food = self.get_by_id(id)

        if food_data.food_type_id:
            type_deleted = self.db.query(FoodTypes).filter(FoodTypes.id == food_data.food_type_id)\
                            .filter(FoodTypes.deleted_at.is_not(None)).first()

            if type_deleted:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Dữ liệu loại thức ăn {type_deleted.code}{' '}{type_deleted.name} đã bị xóa.",
            )

        if food_data.supplier_id:
            supplier_deleted = self.db.query(Suppliers).filter(Suppliers.id == food_data.supplier_id)\
                            .filter(Suppliers.deleted_at.is_not(None)).first()

            if supplier_deleted:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Dữ liệu nhà cung cấp {supplier_deleted.supplier_code}{' '}{supplier_deleted.name} đã bị xóa.",
            )

        if food_data.protein_value:
            if food_data.protein_value < 0:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Giá trị độ đạm phải là số nguyên dương"
                    )

        if food_data.fish_type_id:
            fish_type = self.db.query(FishTypes).filter(and_(FishTypes.id == food_data.fish_type_id, FishTypes.deleted_at.is_(None))).first()

            if not fish_type:
                raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Loại cá không tồn tại hoặc đã bị xóa",
            )


        self.db.query(Foods).filter(Foods.id == id).update(food_data.dict())
        self.db.commit()

        return food

    def update_status(self, id: int, food_status: FoodStatusUpdateRequest):
        food = self.get_by_id(id)
        self.db.query(Foods).filter(Foods.id == id).update(food_status.dict())
        self.db.commit()

        return food

    def delete_fish_food(self, id: int):
        self.get_by_id(id)
        fish_food_images = self.db.query(Images) \
            .filter(Images.record_id == id,Images.record_type == type.fish_food_types).all()
        for img in fish_food_images:
            ImagesService.delete_file_s3(img.file_name)
        self.db.query(Foods).filter(Foods.id == id).delete(synchronize_session=False)
        self.db.commit()
     

    def upload_food_image(self, food_id: int, image_data: UploadFile = File(...), food_subtype: FoodImageSubType = None):
        food = self.db.query(Foods).filter(Foods.id == food_id).first()

        if not food:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Thức ăn không tồn tại.",
            )

        image_tail = image_file(image_data)
        filename = ImagesService.upload_photo_s3(image_data)
        image_url = f'{settings.s3_endpoint}/{filename}'
        record_type = ImagesType.fish_food_types

        ImagesService.upload_image(self, food_id, record_type, image_tail, filename, image_url, food_subtype)

        self.db.commit()

    
    def upload_multi_food_image(self, food_id: int, image_datas: List[UploadFile] = File(...), food_subtype: FoodImageSubType = None):
        food = self.db.query(Foods).filter(Foods.id == food_id).first()

        if not food:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Thức ăn không tồn tại.",
            )

        for img in image_datas:
            image_tail = image_file(img)
            filename = ImagesService.upload_photo_s3(img)
            image_url = f'{settings.s3_endpoint}/{filename}'
            record_type = ImagesType.fish_food_types

            ImagesService.upload_image(self, food_id, record_type, image_tail, filename, image_url, food_subtype)

        self.db.commit()

    
    def soft_delete_food(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        food_in = self.db.query(FoodIn).filter(and_(FoodIn.food_id == id, FoodIn.inventory > 0)).all()

        if food_in:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Thức ăn vẫn còn trong kho."
            )

        self.db.query(Foods).filter(Foods.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()
