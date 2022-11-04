from sqlalchemy import desc, and_
from sqlalchemy.sql import func
from app.core.service import BaseService
from app.models.medicine_in import MedicineIn
from app.models.medicine_out import MedicineOut
from app.schemas.medicine_in import MedicineInCreate, MedicineInFilter, MedicineInUpdateRequest
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from app.models.specification import Specifications
from app.models.unit import Units


class MedicineInsService(BaseService):

    def get_by_id(self, id: int):
        medicine_in = self.db.query(MedicineIn).filter(MedicineIn.id == id).first()

        if not medicine_in:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Medicine with id: {id} does not exist",
                            'code': 'ER0041'
                        }]
                )
        return medicine_in


    def create(self, medicine_in_data: MedicineInCreate):
        
        last_record = self.db.query(MedicineIn).filter(MedicineIn.medicine_id == medicine_in_data.medicine_id)\
                            .filter(MedicineIn.adopt_area_id == medicine_in_data.adopt_area_id)\
                            .filter(MedicineIn.in_date == medicine_in_data.in_date)\
                            .order_by(desc(MedicineIn.id)).first()
        date_code = medicine_in_data.in_date.strftime("%d-%m-%y").replace('-', '')
        prefix = f'{"TH-"}{date_code}{"-"}'
        if last_record is None:
            code = f'{prefix}{0}{1}'
        else:
            temp = last_record.batch_code[:10]
            index = last_record.batch_code.replace(temp,'')
            index = int(index) + 1
            if index < 10:
                code = f'{prefix}{0}{index}'
            else:
                code = f'{prefix}{index}'

        specification = self.db.query(Specifications).filter(and_(Specifications.id == medicine_in_data.specification_id, Specifications.deleted_at.is_(None))).first()

        if not specification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Qui cách không tồn tại")

        quantity = medicine_in_data.amount * specification.amount

        new_medicine_in = MedicineIn(
            batch_code=code,
            medicine_id=medicine_in_data.medicine_id,
            adopt_area_id=medicine_in_data.adopt_area_id,
            quantity=quantity,
            inventory=quantity,
            unit_id=medicine_in_data.unit_id,
            in_date=medicine_in_data.in_date,
            mfg_date=medicine_in_data.mfg_date,
            exp_date=medicine_in_data.exp_date,
            specification_id=medicine_in_data.specification_id
        )
        self.db.add(new_medicine_in)
        self.db.commit()
        self.db.refresh(new_medicine_in)

        return new_medicine_in


    def update(self, id, medicine_in_data: MedicineInUpdateRequest):
        medicine_in = self.get_by_id(id)
        medicine_in_query = self.db.query(MedicineIn).filter(MedicineIn.id == id)
        medicine_in_quantity = medicine_in_query.join(MedicineIn.specification).first()

        if medicine_in_data.amount and medicine_in_quantity:
            medicine_in_quantity_value = medicine_in_quantity.specification.amount * medicine_in_data.amount

            total_quantity_medicine_out = self.db.query(func.sum(MedicineOut.quantity).label("total_score")).filter(MedicineOut.medicine_in_id ==id).scalar()

            if total_quantity_medicine_out:
                if medicine_in_quantity_value < total_quantity_medicine_out:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"{total_quantity_medicine_out}"
                    )
                inventory = medicine_in_quantity_value - total_quantity_medicine_out
                medicine_in_query.update({"inventory": inventory}, synchronize_session=False)
                self.db.query(MedicineOut).filter(MedicineOut.medicine_in_id == id).update({"inventory": inventory}, synchronize_session=False)
            else:
                medicine_in_query.update({"inventory": medicine_in_quantity_value}, synchronize_session=False)

            medicine_in_query.update({"quantity": medicine_in_quantity_value}, synchronize_session=False)

        if medicine_in_data.unit_id:
            unit_deleted = self.db.query(Units).filter(and_(Units.id == medicine_in_data.unit_id, Units.deleted_at.is_not(None))).first()

            if unit_deleted:
                raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'toast': f"Đơn vị đã bị xóa."
                        }]
                    )

            medicine_in_query.update({"unit_id": medicine_in_data.unit_id}, synchronize_session=False)

        if medicine_in_data.mfg_date:
            medicine_in_query.update({"mfg_date": medicine_in_data.mfg_date}, synchronize_session=False)

        if medicine_in_data.exp_date:
            medicine_in_query.update({"exp_date": medicine_in_data.exp_date}, synchronize_session=False)

        if medicine_in_data.in_date:
            if medicine_in_data.in_date != medicine_in.in_date:
                last_record = self.db.query(MedicineIn).filter(MedicineIn.medicine_id == medicine_in.medicine_id)\
                                .filter(MedicineIn.adopt_area_id == medicine_in.adopt_area_id)\
                                .filter(MedicineIn.in_date == medicine_in_data.in_date)\
                                .order_by(desc(MedicineIn.id)).first()

                date_code = medicine_in_data.in_date.strftime("%d-%m-%y").replace('-', '')
                prefix = f'{"TH-"}{date_code}{"-"}'

                if last_record is None:
                    code = f'{prefix}{0}{1}'
                else:
                    temp = last_record.batch_code[:10]
                    index = last_record.batch_code.replace(temp,'')
                    index = int(index) + 1
                    if index < 10:
                        code = f'{prefix}{0}{index}'
                    else:
                        code = f'{prefix}{index}'
                        
                medicine_in_query.update({"in_date": medicine_in_data.in_date}, synchronize_session=False)
                medicine_in_query.update({"batch_code": code}, synchronize_session=False)

        self.db.commit()

        return medicine_in

    def get_all(self, medicine_in_filter: MedicineInFilter, all = False):
        query = self.db.query(MedicineIn)

        if medicine_in_filter.adopt_area_id:
            query = query.filter(MedicineIn.adopt_area_id == medicine_in_filter.adopt_area_id)

        if medicine_in_filter.medicine_id:
            query = query.filter(MedicineIn.medicine_id == medicine_in_filter.medicine_id)

        if medicine_in_filter.from_date:
            query = query.filter(MedicineIn.created_at >= medicine_in_filter.from_date.date())

        if medicine_in_filter.to_date:
            to_date = medicine_in_filter.to_date + timedelta(days=1)
            query = query.filter(MedicineIn.created_at <= to_date.date())

        if medicine_in_filter.out_of_inventory:
            query = query.filter(MedicineIn.inventory != 0)

        query = query.order_by(desc(MedicineIn.created_at))

        if all == False:
            if medicine_in_filter.limit:
                query = query.limit(medicine_in_filter.limit)

            if medicine_in_filter.offset:
                query = query.offset(medicine_in_filter.offset)

        return query.all()

