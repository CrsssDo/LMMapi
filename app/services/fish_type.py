from datetime import datetime
from app.core.service import BaseService
from app.models.fish_type import FishTypes
from app.schemas.fish_type import FishTypesResponse
from fastapi import HTTPException, status, Response
from sqlalchemy import and_


class FishTypesService(BaseService):

    def get_by_id(self, id:int):
        fish_type = self.db.query(FishTypes).filter(FishTypes.id == id).first()

        if not fish_type:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Fish type with id: {id} does not exist",
                            'code': 'ER0035'
                        }]
                )
        return fish_type


    def create(self, name: str):
        fish_type = self.db.query(FishTypes).filter(and_(FishTypes.name == name, FishTypes.deleted_at.is_(None))).first()

        if fish_type:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu loại cá đã tồn tại",
                            'code': 'ER0036'
                        }]
                )

        max_id = self.db.execute("""
                select max(id) from fish_types 
                """).first()
        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'LCA-'
        if generate < 10:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

    
        new_fish_type = FishTypes(
            code=code,
            name=name
        )
        self.db.add(new_fish_type)
        self.db.commit()
        self.db.refresh(new_fish_type)

        return new_fish_type


    def get_all(self):
        fish_types = self.db.query(FishTypes)

        fish_types = fish_types.filter(FishTypes.deleted_at.is_(None))

        return fish_types.order_by(FishTypes.code).all()

    def update_fish_type(self, id:int, name: str):
        fish_type = self.get_by_id(id)
        if name:
            fish_type_exist = self.db.query(FishTypes).filter(and_(FishTypes.name == name, FishTypes.deleted_at.is_(None))).first()
            if fish_type_exist:
                if fish_type.id != fish_type_exist.id:
                    raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu loại cá đã tồn tại",
                            'code': 'ER0036'
                        }]
                )
            self.db.query(FishTypes).filter(FishTypes.id == id).update({"name": name}, synchronize_session=False)

        self.db.commit()

        return fish_type


    def soft_delete_fish_type(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        self.db.query(FishTypes).filter(FishTypes.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()






    
