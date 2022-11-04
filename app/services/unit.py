from datetime import datetime
from app.core.service import BaseService
from app.models.unit import Units
from app.schemas.unit import UnitCreateRequest, UnitUpdateRequest
from fastapi import HTTPException, status, Response
from sqlalchemy import and_


class UnitsService(BaseService):

    def get_by_id(self, id:int):
        unit = self.db.query(Units).filter(Units.id == id).first()

        if not unit:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Unit with id: {id} does not exist",
                            'code': 'ER0057'
                        }]
                )
        return unit


    def create(self, unit_data:UnitCreateRequest):
        exist_unit = self.db.query(Units).filter(and_(Units.code == unit_data.code, Units.deleted_at.is_(None))).first()

        if exist_unit:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Đơn vị đã tồn tại",
                            'code': 'ER0058'
                        }]
                )

        max_id = self.db.execute("""
        select max(id) from units 
        """).first()

        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'DV-'
        if generate < 10:
            code = f'{prefix}{0}{0}{generate}'
        elif generate >= 10 and generate < 100:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_unit = Units(
            unit_code=code,
            code=unit_data.code,
            description=unit_data.description
        )

        self.db.add(new_unit)
        self.db.commit()
        self.db.refresh(new_unit)

        return new_unit


    def get_all(self):
        units = self.db.query(Units)

        units = units.filter(Units.deleted_at.is_(None))

        return units.order_by(Units.code).all()

    def update_unit(self, id:int, unit_data: UnitUpdateRequest):
        unit = self.get_by_id(id)
        if unit.code != unit_data.code:
            exist_unit = self.db.query(Units).filter(and_(Units.code == unit_data.code, Units.deleted_at.is_(None))).first()

            if exist_unit:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Đơn vị đã tồn tại",
                            'code': 'ER0058'
                        }]
                )
        self.db.query(Units).filter(Units.id == id).update(unit_data.dict())
        self.db.commit()

        return unit

    def soft_delete_unit(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        self.db.query(Units).filter(Units.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()






    
