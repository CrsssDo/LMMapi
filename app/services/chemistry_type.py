from datetime import datetime
from app.core.service import BaseService
from app.models.chemistry_type import ChemistryTypes
from app.schemas.chemistry_type import ChemistryTypesResponse
from fastapi import HTTPException, status, Response
from sqlalchemy import and_


class ChemistryTypesService(BaseService):

    def get_by_id(self, id:int):
        chemistry_type = self.db.query(ChemistryTypes).filter(ChemistryTypes.id == id).first()

        if not chemistry_type:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Chemistry out with id: {id} does not exist",
                            'code': 'ER0011'
                        }]
                )
        return chemistry_type


    def create(self, name: str):
        chemistry_type = self.db.query(ChemistryTypes).filter(and_(ChemistryTypes.name == name, ChemistryTypes.deleted_at.is_(None))).first()

        if chemistry_type:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Loại hóa chất đã tồn tại"
                )

        max_id = self.db.execute("""
                select max(id) from chemistry_types 
                """).first()
        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'LHC-'
        if generate < 10:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

    
        new_chemistry_type = ChemistryTypes(
            code=code,
            name=name
        )
        self.db.add(new_chemistry_type)
        self.db.commit()
        self.db.refresh(new_chemistry_type)

        return new_chemistry_type


    def get_all(self):
        chemistry_types = self.db.query(ChemistryTypes)

        chemistry_types = chemistry_types.filter(ChemistryTypes.deleted_at.is_(None))

        return chemistry_types.order_by(ChemistryTypes.code).all()

    def update_chemistry_type(self, id:int, name: str):
        chemistry_type = self.get_by_id(id)
        if name:
            chemistry_type_exist = self.db.query(ChemistryTypes).filter(and_(ChemistryTypes.name == name, ChemistryTypes.deleted_at.is_(None))).first()
            if chemistry_type_exist:
                if chemistry_type.id != chemistry_type_exist.id:
                    raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu loại hóa chất đã tồn tại",
                            'code': 'ER0012'
                        }]
                )

            self.db.query(ChemistryTypes).filter(ChemistryTypes.id == id).update({"name": name}, synchronize_session=False)

        self.db.commit()

        return chemistry_type


    def soft_delete_chemistry_type(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        self.db.query(ChemistryTypes).filter(ChemistryTypes.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()






    
