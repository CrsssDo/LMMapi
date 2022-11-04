from datetime import datetime, timedelta
from sqlalchemy import desc, and_
from sqlalchemy.sql import func
from app.core.service import BaseService
from app.models.chemistry_in import ChemistryIns
from app.models.chemistry_out import ChemistryOuts
from app.models.food_in import FoodIn
from app.schemas.chemistry_in import ChemistryInCreateRequest, ChemistryInFilter, ChemistryInUpdateRequest
from fastapi import HTTPException, status
from app.models.unit import Units
from app.models.specification import Specifications


class ChemistryInService(BaseService):

    def get_by_id(self, id: int):
        chemistry_in = self.db.query(ChemistryIns).filter(ChemistryIns.id == id).first()

        if not chemistry_in:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Chemistry in with id: {id} does not exist",
                            'code': 'ER0007'
                        }]
                ) 

        return chemistry_in


    def create(self, chemistry_in_data: ChemistryInCreateRequest):

        last_record = self.db.query(ChemistryIns).filter(ChemistryIns.chemistry_id == chemistry_in_data.chemistry_id)\
                            .filter(ChemistryIns.adopt_area_id == chemistry_in_data.adopt_area_id)\
                            .filter(ChemistryIns.in_date == chemistry_in_data.in_date)\
                            .order_by(desc(ChemistryIns.id)).first()
        date_code = chemistry_in_data.in_date.strftime("%d-%m-%y").replace('-', '')
        prefix = f'{"HC-"}{date_code}{"-"}'
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

        specification = self.db.query(Specifications).filter(and_(Specifications.id == chemistry_in_data.specification_id, Specifications.deleted_at.is_(None))).first()

        if not specification:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Qui cách không tồn tại",
                            'code': 'ER0008'
                        }]
                )
            
            
        quantity = chemistry_in_data.amount * specification.amount


        new_chemistry_in = ChemistryIns(
            batch_code=code,
            chemistry_id=chemistry_in_data.chemistry_id,
            adopt_area_id=chemistry_in_data.adopt_area_id,
            quantity=quantity,
            inventory=quantity,
            unit_id=chemistry_in_data.unit_id,
            in_date=chemistry_in_data.in_date,
            mfg_date=chemistry_in_data.mfg_date,
            exp_date=chemistry_in_data.exp_date,
            specification_id=chemistry_in_data.specification_id
        )
        self.db.add(new_chemistry_in)
        self.db.commit()
        self.db.refresh(new_chemistry_in)

        return new_chemistry_in


    def update(self, id, chemistry_in_data: ChemistryInUpdateRequest):
        chemistry_in = self.get_by_id(id)
        chemistry_in_query = self.db.query(ChemistryIns).filter(ChemistryIns.id == id)
        chemistry_in_quantity = chemistry_in_query.join(ChemistryIns.specification).first()


        if chemistry_in_data.amount and chemistry_in_quantity:
            chemistry_in_quantity_value = chemistry_in_quantity.specification.amount * chemistry_in_data.amount

            total_quantity_chemistry_out = self.db.query(func.sum(ChemistryOuts.quantity).label("total_score")).filter(ChemistryOuts.chemistry_in_id ==id).scalar()

            if total_quantity_chemistry_out:
                if chemistry_in_quantity_value < total_quantity_chemistry_out:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"{int(total_quantity_chemistry_out)}"
                    )
                inventory = chemistry_in_quantity_value - total_quantity_chemistry_out
                chemistry_in_query.update({"inventory": inventory}, synchronize_session=False)
                self.db.query(ChemistryOuts).filter(ChemistryOuts.chemistry_in_id == id).update({"inventory": inventory}, synchronize_session=False)
            else:
                chemistry_in_query.update({"inventory": chemistry_in_quantity_value}, synchronize_session=False)

            chemistry_in_query.update({"quantity": chemistry_in_quantity_value}, synchronize_session=False)

        if chemistry_in_data.unit_id:
            unit_deleted = self.db.query(Units).filter(and_(Units.id == chemistry_in_data.unit_id, Units.deleted_at.is_not(None))).first()

            if unit_deleted:
                raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'toast': f"Đơn vị đã bị xóa."
                        }]
                    )

            chemistry_in_query.update({"unit_id": chemistry_in_data.unit_id}, synchronize_session=False)

        if chemistry_in_data.mfg_date:
            chemistry_in_query.update({"mfg_date": chemistry_in_data.mfg_date}, synchronize_session=False)

        if chemistry_in_data.exp_date:
            chemistry_in_query.update({"exp_date": chemistry_in_data.exp_date}, synchronize_session=False)

        if chemistry_in_data.in_date:
            if chemistry_in_data.in_date != chemistry_in.in_date:
                last_record = self.db.query(ChemistryIns).filter(ChemistryIns.chemistry_id == chemistry_in.chemistry_id)\
                                .filter(ChemistryIns.adopt_area_id == chemistry_in.adopt_area_id)\
                                .filter(ChemistryIns.in_date == chemistry_in_data.in_date)\
                                .order_by(desc(ChemistryIns.id)).first()

                date_code = chemistry_in_data.in_date.strftime("%d-%m-%y").replace('-', '')
                prefix = f'{"HC-"}{date_code}{"-"}'

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
                        
                chemistry_in_query.update({"in_date": chemistry_in_data.in_date}, synchronize_session=False)
                chemistry_in_query.update({"batch_code": code}, synchronize_session=False)

        self.db.commit()

        return chemistry_in

    def get_all(self, chemistry_filter_data: ChemistryInFilter, all = False):
        query = self.db.query(ChemistryIns)

        if chemistry_filter_data.from_date:
            query = query.filter(ChemistryIns.created_at >= chemistry_filter_data.from_date.date())

        if chemistry_filter_data.to_date:
            to_date = chemistry_filter_data.to_date + timedelta(days=1)
            query = query.filter(ChemistryIns.created_at <= to_date.date())

        if chemistry_filter_data.chemistry_id:
            query = query.filter(ChemistryIns.chemistry_id == chemistry_filter_data.chemistry_id)

        if chemistry_filter_data.adopt_area_id:
            query = query.filter(ChemistryIns.adopt_area_id == chemistry_filter_data.adopt_area_id)

        if chemistry_filter_data.out_of_inventory:
            query = query.filter(ChemistryIns.inventory != 0)

        query = query.order_by(desc(ChemistryIns.created_at))

        if all == False:
            if chemistry_filter_data.limit:
                query = query.limit(chemistry_filter_data.limit)
            if chemistry_filter_data.offset:
                query = query.offset(chemistry_filter_data.offset)
                
        return query.all()

        


