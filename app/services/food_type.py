from datetime import datetime
from app.core.service import BaseService
from app.models.food_type import FoodTypes
from app.schemas.food_type import FoodTypesResponse
from fastapi import HTTPException, status, Response
from sqlalchemy import and_


class FoodTypesService(BaseService):

    def get_by_id(self, id:int):
        food_type = self.db.query(FoodTypes).filter(FoodTypes.id == id).first()

        if not food_type:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Food type with id: {id} does not exist",
                            'code': 'ER0034'
                        }]
                )
    
        return food_type


    def create(self, name: str):
        food_type = self.db.query(FoodTypes).filter(and_(FoodTypes.name == name, FoodTypes.deleted_at.is_(None))).first()

        if food_type:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Loại thức ăn đã tồn tại"
                )

        max_id = self.db.execute("""
                select max(id) from food_types 
                """).first()
        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'LTA-'
        if generate < 10:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

    
        new_food_type = FoodTypes(
            code=code,
            name=name
        )
        self.db.add(new_food_type)
        self.db.commit()
        self.db.refresh(new_food_type)

        return new_food_type


    def get_all(self):
        food_types = self.db.query(FoodTypes)

        food_types = food_types.filter(FoodTypes.deleted_at.is_(None))

        return food_types.order_by(FoodTypes.code).all()

    def update_food_type(self, id:int, name: str):
        food_type = self.get_by_id(id)
        if name:
            food_type_exist = self.db.query(FoodTypes).filter(and_(FoodTypes.name == name, FoodTypes.deleted_at.is_(None))).first()
            if food_type_exist:
                if food_type.id != food_type_exist.id:
                    raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Dữ liệu loại thức ăn đã tồn tại",
                    )
            self.db.query(FoodTypes).filter(FoodTypes.id == id).update({"name": name}, synchronize_session=False)

        self.db.commit()

        return food_type


    def soft_delete_food_type(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        self.db.query(FoodTypes).filter(FoodTypes.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()






    
