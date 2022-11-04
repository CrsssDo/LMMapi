from datetime import datetime
from app.core.service import BaseService
from app.models.medicine_type import MedicineTypes
from app.schemas.medicine_type import MedicineTypesResponse
from fastapi import HTTPException, status, Response
from sqlalchemy import and_


class MedicineTypesService(BaseService):

    def get_by_id(self, id:int):
        medicine_type = self.db.query(MedicineTypes).filter(MedicineTypes.id == id).first()

        if not medicine_type:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Medicine type with id: {id} does not exist",
                            'code': 'ER0043'
                        }]
                )
        return medicine_type


    def create(self, name: str):
        medicine_type = self.db.query(MedicineTypes).filter(and_(MedicineTypes.name == name, MedicineTypes.deleted_at.is_(None))).first()

        if medicine_type:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Loại thuốc đã tồn tại",
                            'code': 'ER0044'
                        }]
                )

        max_id = self.db.execute("""
                select max(id) from medicine_types 
                """).first()
        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'LTH-'
        if generate < 10:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

    
        new_medicine_type = MedicineTypes(
            code=code,
            name=name
        )
        self.db.add(new_medicine_type)
        self.db.commit()
        self.db.refresh(new_medicine_type)

        return new_medicine_type


    def get_all(self):
        medicine_types = self.db.query(MedicineTypes)

        medicine_types = medicine_types.filter(MedicineTypes.deleted_at.is_(None))

        return medicine_types.order_by(MedicineTypes.code).all()

    def update_medicine_type(self, id:int, name: str):
        medicine_type = self.get_by_id(id)
        if name:
            medicine_type_exist = self.db.query(MedicineTypes).filter(and_(MedicineTypes.name == name, MedicineTypes.deleted_at.is_(None))).first()
            if medicine_type_exist:
                if medicine_type.id != medicine_type_exist.id:
                    raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Loại thuốc đã tồn tại",
                            'code': 'ER0044'
                        }]
                )
            self.db.query(MedicineTypes).filter(MedicineTypes.id == id).update({"name": name}, synchronize_session=False)

        self.db.commit()

        return medicine_type


    def soft_delete_medicine_type(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        self.db.query(MedicineTypes).filter(MedicineTypes.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()






    
