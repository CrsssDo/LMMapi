from datetime import date, datetime, timedelta
from sqlalchemy import desc, cast, Date
from app.core.service import BaseService
from app.models.chemistry_out import ChemistryOuts
from app.models.chemistry_in import ChemistryIns
from app.models.pond import Ponds
from app.schemas.chemistry_out import ChemistryOutCreate, ChemistryOutFilter, ChemistryOutHistoryValue, ChemistryOutHistoryResponse
from fastapi import HTTPException, status
from app.models.adopt import AdoptAreas


class ChemistryOutService(BaseService):

    def get_by_id(self, id: int):
        chemistry_out = self.db.query(ChemistryOuts).filter(ChemistryOuts.id == id).first()

        if not chemistry_out:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Chemistry out with id: {id} does not exist",
                            'code': 'ER0009'
                        }]
                )
        return chemistry_out


    def create(self, chemistry_out_data: ChemistryOutCreate):
        pond_query = self.db.query(Ponds).filter(Ponds.id == chemistry_out_data.pond_id).first()

        chemistry_in = self.db.query(ChemistryIns).filter(ChemistryIns.id == chemistry_out_data.chemistry_in_id).first()

        date_now = datetime.now().date()
        min_date = date_now - timedelta(days=2)

        if(chemistry_in.in_date > min_date):
            min_date = chemistry_in.in_date

        if chemistry_out_data.in_date:
            if chemistry_out_data.in_date < min_date or chemistry_out_data.in_date > date_now:
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    [{
                            'error' : True,
                            'message': f"Ngày xuất phải từ ngày {min_date.day}{'/'}{min_date.month} đến {date_now.day}{'/'}{date_now.month}",
                            'code': 'ER0010'
                        }]
                )

        if pond_query.status == False:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'pond': f"Bể vừa chọn đang được bảo trì.",
                    'type': 'type_error.invalid'
                }]
            )

        chemistry_in_query = self.db.query(ChemistryIns).filter(ChemistryIns.id == chemistry_out_data.chemistry_in_id)
        chemistry_in = chemistry_in_query.first()

        inventory_limit = chemistry_in.inventory - chemistry_out_data.quantity

        if inventory_limit < 0:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'quantity': f"Số lượng vượt quá giới hạn.",
                    'type': 'type_error.invalid'
                }]
            )
        else:
            chemistry_in_query.update({"inventory": inventory_limit}, synchronize_session=False)

        new_chemistry_out = ChemistryOuts(
            chemistry_in_id=chemistry_out_data.chemistry_in_id,
            quantity=chemistry_out_data.quantity,
            inventory=inventory_limit,
            pond_id=chemistry_out_data.pond_id,
            in_date=chemistry_out_data.in_date,
            note=chemistry_out_data.note
        )
        self.db.add(new_chemistry_out)
        self.db.commit()
        self.db.refresh(new_chemistry_out)

        return new_chemistry_out


    def get_all(self, chemistry_filter_data: ChemistryOutFilter, all = False):
        query = self.db.query(ChemistryOuts).join(ChemistryOuts.chemistry_in)

        if chemistry_filter_data.chemistry_id:
            query = query.filter(ChemistryIns.chemistry_id == chemistry_filter_data.chemistry_id)

        if chemistry_filter_data.adopt_area_id:
            query = query.filter(ChemistryIns.adopt_area_id == chemistry_filter_data.adopt_area_id)

        if chemistry_filter_data.chemistry_in_id:
            query = query.filter(ChemistryOuts.chemistry_in_id == chemistry_filter_data.chemistry_in_id)

        if chemistry_filter_data.pond_id:
            query = query.filter(ChemistryOuts.pond_id == chemistry_filter_data.pond_id)

        query = query.order_by(desc(ChemistryOuts.created_at))

        if all == False:
            if chemistry_filter_data.limit:
                query = query.limit(chemistry_filter_data.limit)

            if chemistry_filter_data.offset:
                query = query.offset(chemistry_filter_data.offset)
                
        return query.all()

    def get_total_quantity_medicine_out_for_pond(self, pond_id: int):
        chemistry_out = self.db.query(ChemistryOuts).filter(ChemistryOuts.pond_id == pond_id).all()

        total_quantity = 0
        for i in chemistry_out:
            total_quantity += i.quantity

        return total_quantity


    def get_chemistry_out_history(self, pond_id: int):
        chemistry_out_history_date = self.db.query(cast(ChemistryOuts.created_at, Date).label("in_date"))\
                                            .filter(ChemistryOuts.pond_id == pond_id).order_by(desc("in_date")).distinct().all()                                           

        chemistry_outs = self.db.query(ChemistryOuts).filter(ChemistryOuts.pond_id == pond_id).all()

        chemistry_out_history_datas = []

        for i in chemistry_out_history_date:
            chemistry_out_data = []
            for j in chemistry_outs:
                if i.in_date == j.created_at.date():
                    if j.chemistry_in.chemistry.supplier and j.chemistry_in.unit:
                        name = f'{j.chemistry_in.chemistry.name}{" "}{j.chemistry_in.chemistry.supplier.name}{" "}{"("}{j.chemistry_in.unit.code}{")"}'
                    else:
                        name = f'{j.chemistry_in.chemistry.name}'

                    chemistry_out_data.append(ChemistryOutHistoryValue(id=j.id, name=name, batch_code=j.chemistry_in.batch_code, quantity=j.quantity, note=j.note))

            chemistry_out_history_datas.append(ChemistryOutHistoryResponse(in_date=i.in_date, history_datas=chemistry_out_data))

        return chemistry_out_history_datas

