from datetime import datetime
from sqlalchemy import and_
from app.core.service import BaseService
from app.models.supplier import SupplierTypes, Suppliers
from app.schemas.supplier import SupplierUpdateRequest, SupplierCreateRequest
from fastapi import HTTPException, status, Response
from app.utils.generate import generate_code
from app.models.base_season_pond import BaseSeasonPonds


class SuppliersService(BaseService):

    def get_by_id(self, id: int):
        supplier = self.db.query(Suppliers).filter(Suppliers.id == id).first()

        if not supplier:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Supplier with id: {id} does not exist",
                            'code': 'ER0055'
                        }]
                )
        return supplier

    def create(self, supplier_data: SupplierCreateRequest):
        max_id = self.db.execute("""
        select max(id) from suppliers 
        """).first()

        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'NCC-'
        if generate < 10:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_supplier = Suppliers(
            supplier_code=code,
            name=supplier_data.name,
            address=supplier_data.address,
            address_level_1_id=supplier_data.address_level_1_id,
            supplier_type_id=supplier_data.supplier_type_id
        )
        self.db.add(new_supplier)
        self.db.commit()
        self.db.refresh(new_supplier)

        return new_supplier

    def get_all(self):
        suppliers = self.db.query(Suppliers)

        suppliers = suppliers.filter(Suppliers.deleted_at.is_(None))

        return suppliers.order_by(Suppliers.supplier_code).all()

    def update_supplier(self, id: int, supplier_data: SupplierUpdateRequest):
        supplier = self.get_by_id(id)
        self.db.query(Suppliers).filter(Suppliers.id == id).update(supplier_data.dict())
        self.db.commit()

        return supplier

    def delete_supplier(self, id: int):
        self.get_by_id(id)
        self.db.query(Suppliers).filter(Suppliers.id == id).delete(synchronize_session=False)

        self.db.commit()

    def soft_delete_supplier(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        supplier_in_base_season = self.db.query(BaseSeasonPonds).filter(and_(BaseSeasonPonds.supplier_id == id, BaseSeasonPonds.status.not_in(['Kết thúc','Đã hủy']))).all()

        if supplier_in_base_season:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Nhà cung cấp đang dùng trong vụ nuôi",
                            'code': 'ER0056'
                        }]
                )

        self.db.query(Suppliers).filter(Suppliers.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()
        

class SupplierTypesService(BaseService):

    def get_all(self):
        supplier_types = self.db.query(SupplierTypes).all()
        return supplier_types

