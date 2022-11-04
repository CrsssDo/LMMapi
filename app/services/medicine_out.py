from datetime import datetime, timedelta
from sqlalchemy import Date, desc, cast
from sqlalchemy import desc
from app.core.service import BaseService
from app.models.medicine_out import MedicineOut
from app.models.medicine_in import MedicineIn
from app.models.pond import Ponds
from app.models.adopt import AdoptAreas
from app.schemas.medicine_out import MedicineOutCreate, MedicineOutFilter, MedicineOutHistoryValue, MedicineOutHistoryResponse
from fastapi import HTTPException, status


class MedicineOutsService(BaseService):

    def get_by_id(self, id: int):
        medicine_out = self.db.query(MedicineOut).filter(MedicineOut.id == id).first()

        if not medicine_out:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Medicine out with id: {id} does not exist",
                            'code': 'ER0042'
                        }]
                )

        return medicine_out

    def create(self, medicine_out_data: MedicineOutCreate):
        pond_query = self.db.query(Ponds).filter(Ponds.id == medicine_out_data.pond_id).first()

        medicine_in = self.db.query(MedicineIn).filter(MedicineIn.id == medicine_out_data.medicine_in_id).first()

        date_now = datetime.now().date()
        min_date = date_now - timedelta(days=2)

        if(medicine_in.in_date > min_date):
            min_date = medicine_in.in_date

        if medicine_out_data.in_date:
            if medicine_out_data.in_date < min_date or medicine_out_data.in_date > date_now:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Ngày xuất phải từ ngày {min_date.day}{'/'}{min_date.month} đến {date_now.day}{'/'}{date_now.month}"
                )

        if pond_query.status == False:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'pond': f"Bể vừa chọn đang được bảo trì.",
                    'type': 'type_error.invalid'
                }]
            )

        medicine_in_query = self.db.query(MedicineIn).filter(MedicineIn.id == medicine_out_data.medicine_in_id)
        medicine_in = medicine_in_query.first()

        inventory_limit = medicine_in.inventory - medicine_out_data.quantity

        if inventory_limit < 0:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'quantity': f"Số lượng vượt quá giới hạn.",
                    'type': 'type_error.invalid'
                }]
            )
        else:
            medicine_in_query.update({"inventory": inventory_limit}, synchronize_session=False)
        
        new_medicine_out = MedicineOut(
            medicine_in_id=medicine_out_data.medicine_in_id,
            quantity=medicine_out_data.quantity,
            inventory=inventory_limit,
            pond_id=medicine_out_data.pond_id,
            in_date=medicine_out_data.in_date,
            note=medicine_out_data.note
        )
        self.db.add(new_medicine_out)
        self.db.commit()
        self.db.refresh(new_medicine_out)

        return new_medicine_out


    def get_all(self, medicine_filter_data: MedicineOutFilter, all = False):
        query = self.db.query(MedicineOut).join(MedicineIn, MedicineIn.id == MedicineOut.medicine_in_id)

        if medicine_filter_data.medicine_id:
            query = query.filter(MedicineIn.medicine_id == medicine_filter_data.medicine_id)

        if medicine_filter_data.adopt_area_id:
            query = query.filter(MedicineIn.adopt_area_id == medicine_filter_data.adopt_area_id)

        if medicine_filter_data.medicine_in_id:
            query = query.filter(MedicineOut.medicine_in_id == medicine_filter_data.medicine_in_id)

        if medicine_filter_data.pond_id:
            query = query.filter(MedicineOut.pond_id == medicine_filter_data.pond_id)

        query = query.order_by(desc(MedicineOut.created_at))

        if all == False:
            if medicine_filter_data.limit:
                query = query.limit(medicine_filter_data.limit)

            if medicine_filter_data.offset:
                query = query.offset(medicine_filter_data.offset)
                
        return query.all()

    def get_total_quantity_medicine_out_for_pond(self, pond_id: int):
        medicine_out = self.db.query(MedicineOut).filter(MedicineOut.pond_id == pond_id).all()

        total_quantity = 0
        for i in medicine_out:
            total_quantity += i.quantity

        return total_quantity

    def get_medicine_out_history(self, pond_id: int):
        medicine_out_history_date = self.db.query(cast(MedicineOut.created_at, Date).label("in_date"))\
                                            .filter(MedicineOut.pond_id == pond_id).order_by(desc("in_date")).distinct().all()                                           

        medicine_outs = self.db.query(MedicineOut).filter(MedicineOut.pond_id == pond_id).all()

        medicine_out_history_datas = []

        for i in medicine_out_history_date:
            medicine_out_data = []
            for j in medicine_outs:
                if i.in_date == j.created_at.date():
                    if j.medicine_in.medicine.supplier and j.medicine_in.specification:
                        name = f'{j.medicine_in.medicine.name}{" - "}{j.medicine_in.medicine.supplier.name}{" "}{"("}{j.medicine_in.specification.unit.code}{")"}'
                    else:
                        name = f'{j.medicine_in.medicine.name}'

                    medicine_out_data.append(MedicineOutHistoryValue(id=j.id, name=name, batch_code=j.medicine_in.batch_code, quantity=j.quantity, note=j.note))

            medicine_out_history_datas.append(MedicineOutHistoryResponse(in_date=i.in_date, history_datas=medicine_out_data))

        return medicine_out_history_datas

    