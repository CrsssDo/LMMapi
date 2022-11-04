from datetime import datetime, timedelta
from operator import index
from sqlalchemy import desc, and_
from sqlalchemy.sql import func
from app.core.service import BaseService
from app.models.food_in import FoodIn
from app.models.food_out import FoodOut
from app.schemas.food_in import FoodInCreateRequest, FoodInUpdateRequest
from fastapi import HTTPException, status
from app.schemas.food_in import FoodInFilter
from app.models.specification import Specifications


class FoodInService(BaseService):

    def get_by_id(self, id: int):
        food_in = self.db.query(FoodIn).filter(FoodIn.id == id).first()

        if not food_in:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Food batch code with id: {id} does not exist",
                            'code': 'ER0031'
                        }]
                )
            
        return food_in


    def create(self, food_in_data: FoodInCreateRequest):

        last_record = self.db.query(FoodIn).filter(FoodIn.food_id == food_in_data.food_id)\
                            .filter(FoodIn.adopt_area_id == food_in_data.adopt_area_id)\
                            .filter(FoodIn.in_date == food_in_data.in_date)\
                            .order_by(desc(FoodIn.id)).first()
        date_code = food_in_data.in_date.strftime("%d-%m-%y").replace('-', '')
        prefix = f'{"TA-"}{date_code}{"-"}'
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

        specification = self.db.query(Specifications).filter(and_(Specifications.id == food_in_data.specification_id, Specifications.deleted_at.is_(None))).first()

        if not specification:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Qui cách không tồn tại",
                            'code': 'ER0032'
                        }]
                )
            
        quantity = food_in_data.amount * specification.amount

        new_food_in = FoodIn(
            batch_code=code,
            food_id=food_in_data.food_id,
            adopt_area_id=food_in_data.adopt_area_id,
            quantity=quantity,
            inventory=quantity,
            type_code=food_in_data.type_code,
            in_date=food_in_data.in_date,
            mfg_date=food_in_data.mfg_date,
            exp_date=food_in_data.exp_date,
            specification_id=food_in_data.specification_id
        )
        self.db.add(new_food_in)
        self.db.commit()
        self.db.refresh(new_food_in)

        return new_food_in

    def update(self, id, food_in_data: FoodInUpdateRequest):
        food_in = self.get_by_id(id)
        food_in_query = self.db.query(FoodIn).filter(FoodIn.id == id)
        food_in_quantity = food_in_query.join(FoodIn.specification).first()


        if food_in_data.amount and food_in_quantity:
            food_in_quantity_value = food_in_quantity.specification.amount * food_in_data.amount

            total_quantity_food_out = self.db.query(func.sum(FoodOut.quantity).label("total_score")).filter(FoodOut.food_in_id ==id).scalar()

            if total_quantity_food_out:
                if food_in_quantity_value < total_quantity_food_out:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"{total_quantity_food_out}"
                    )
                inventory = food_in_quantity_value - total_quantity_food_out
                food_in_query.update({"inventory": inventory}, synchronize_session=False)
                self.db.query(FoodOut).filter(FoodOut.food_in_id == id).update({"inventory": inventory}, synchronize_session=False)
            else:
                food_in_query.update({"inventory": food_in_quantity_value}, synchronize_session=False)

            food_in_query.update({"quantity": food_in_quantity_value}, synchronize_session=False)

        if food_in_data.type_code:
            if food_in_data.type_code > 10:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Loại cỡ không được lớn hơn 10 ly",
                            'code': 'ER0032'
                        }]
                )

            food_in_query.update({"type_code": food_in_data.type_code}, synchronize_session=False)

        if food_in_data.mfg_date:
            food_in_query.update({"mfg_date": food_in_data.mfg_date}, synchronize_session=False)

        if food_in_data.exp_date:
            food_in_query.update({"exp_date": food_in_data.exp_date}, synchronize_session=False)

        if food_in_data.in_date:
            if food_in_data.in_date != food_in.in_date:
                last_record = self.db.query(FoodIn).filter(FoodIn.food_id == food_in.food_id)\
                                .filter(FoodIn.adopt_area_id == food_in.adopt_area_id)\
                                .filter(FoodIn.in_date == food_in_data.in_date)\
                                .order_by(desc(FoodIn.id)).first()

                date_code = food_in_data.in_date.strftime("%d-%m-%y").replace('-', '')
                prefix = f'{"TA-"}{date_code}{"-"}'

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
                        
                food_in_query.update({"in_date": food_in_data.in_date}, synchronize_session=False)
                food_in_query.update({"batch_code": code}, synchronize_session=False)

        self.db.commit()

        return food_in
        

    def get_all(self, food_filter_data: FoodInFilter, all = False):
        query = self.db.query(FoodIn)

        if food_filter_data.from_date:
            query = query.filter(FoodIn.created_at >= food_filter_data.from_date.date())

        if food_filter_data.to_date:
            to_date = food_filter_data.to_date + timedelta(days=1)
            query = query.filter(FoodIn.created_at <= to_date.date())

        if food_filter_data.food_id:
            query = query.filter(FoodIn.food_id == food_filter_data.food_id)

        if food_filter_data.adopt_area_id:
            query = query.filter(FoodIn.adopt_area_id == food_filter_data.adopt_area_id)

        if food_filter_data.out_of_inventory:
            query = query.filter(FoodIn.inventory != 0)

        query = query.order_by(desc(FoodIn.created_at))

        if all == False:
            if food_filter_data.limit:
                query = query.limit(food_filter_data.limit)
            if food_filter_data.offset:
                query = query.offset(food_filter_data.offset)
                
        return query.all()

        


