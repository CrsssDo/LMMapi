from app.core.service import BaseService
from app.models.adopt import AdoptAreas, AdoptAreaTypes, AdoptAreaAdoptTypes
from app.schemas.adopt import AdoptUpdateRequest, AdoptCreateRequest
from fastapi import HTTPException, status
from app.utils.generate import generate_code


class AdoptsService(BaseService):

    def get_by_id(self, id: int):
        adopt = self.db.query(AdoptAreas).filter(AdoptAreas.id == id).first()

        if not adopt:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                        [{
                            'error' : True,
                            'message': f"Vùng nuôi với id: {id} không tồn tại.",
                            'code': 'ER0001'
                        }]
                )
        return adopt

    def create(self, adopt_data: AdoptCreateRequest):

        max_id = self.db.execute("""
        select max(id) from adopt_areas 
        """).first()

        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'VN-'
        if generate < 10:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_adopt = AdoptAreas(
            area_code=code,
            address=adopt_data.address,
            area_owner=adopt_data.area_owner,
            water_environment=adopt_data.water_environment,
            address_level_1_id=adopt_data.address_level_1_id,
        )
        self.db.add(new_adopt)
        self.db.flush()

        for i in adopt_data.adopt_types:
            adopt_type = self.db.query(AdoptAreaTypes).filter(AdoptAreaTypes.id == i).first()
            
            if not adopt_type:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Loại vùng nuôi với id: {id} không tồn tại",
                            'code': 'ER0002'
                        }]
                )

            new_adopt_type = AdoptAreaAdoptTypes(
                adopt_area_id=new_adopt.id,
                adopt_type_id=i
            )
            self.db.add(new_adopt_type)

        self.db.commit()
        self.db.refresh(new_adopt)

        return new_adopt

    def get_all(self):
        adopts = self.db.query(AdoptAreas)
        return adopts.order_by(AdoptAreas.area_code).all()

    def update_adopt(self, id: int, adopt_data: AdoptUpdateRequest):
        adopt = self.get_by_id(id)

        adopt_update = self.db.query(AdoptAreas).filter(AdoptAreas.id == id)

        if adopt_data.area_owner:
            adopt_update.update({"area_owner": adopt_data.area_owner}, synchronize_session=False)

        if adopt_data.address:
            adopt_update.update({"address": adopt_data.address}, synchronize_session=False)

        if adopt_data.address_level_1_id:
            adopt_update.update({"address_level_1_id": adopt_data.address_level_1_id}, synchronize_session=False)

        if adopt_data.water_environment:
            adopt_update.update({"water_environment": adopt_data.water_environment}, synchronize_session=False)

        if adopt_data.adopt_types:
            if adopt.adopt_types:
                self.db.query(AdoptAreaAdoptTypes).filter(AdoptAreaAdoptTypes.adopt_area_id == id).delete()
            
            for i in adopt_data.adopt_types:
                adopt_type = self.db.query(AdoptAreaTypes).filter(AdoptAreaTypes.id == i).first()
        
                if not adopt_type:
                    raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Loại vùng nuôi với id: {id} không tồn tại",
                            'code': 'ER0002'
                        }]
                )

                new_adopt_type = AdoptAreaAdoptTypes(
                    adopt_area_id=id,
                    adopt_type_id=i
                )
                self.db.add(new_adopt_type)

        self.db.commit()

        return adopt


class AdoptTypesService(BaseService):

    def get_all(self):
        adopt_types = self.db.query(AdoptAreaTypes).all()
        return adopt_types

