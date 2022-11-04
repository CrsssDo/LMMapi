from datetime import datetime, timedelta
from sqlalchemy import Date, desc, cast
from app.core.service import BaseService
from app.models.food_out import FoodOut
from app.models.food_in import FoodIn
from app.models.pond import Ponds
from app.schemas.food_out import  FoodOutCreateRequest
from fastapi import HTTPException, status
from app.models.adopt import AdoptAreas
from app.schemas.food_out import FoodOutFilter, FoodOutHistoryValue, FoodOutHistoryResponse


class FoodOutService(BaseService):

    def get_by_id(self, id: int):
        food_out = self.db.query(FoodOut).filter(FoodOut.id == id).first()

        if not food_out:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Food out with id: {id} does not exist",
                            'code': 'ER0033'
                        }]
                )
        
        return food_out


    def create(self, food_out_data: FoodOutCreateRequest):
        pond_query = self.db.query(Ponds).filter(Ponds.id == food_out_data.pond_id).first()

        food_in = self.db.query(FoodIn).filter(FoodIn.id == food_out_data.food_in_id).first()

        date_now = datetime.now().date()
        min_date = date_now - timedelta(days=2)

        if(food_in.in_date > min_date):
            min_date = food_in.in_date

        if food_out_data.in_date:
            if food_out_data.in_date < min_date or food_out_data.in_date > date_now:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Ngày xuất phải từ ngày {min_date.day}{'/'}{min_date.month} đến {date_now.day}{'/'}{date_now.month}",
                            'code': 'ER0034'
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

        food_in_query = self.db.query(FoodIn).filter(FoodIn.id == food_out_data.food_in_id)
        food_in = food_in_query.first()

        inventory_limit = food_in.inventory - food_out_data.quantity

        if inventory_limit < 0:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                [{
                    'quantity': f"Số lượng vượt quá giới hạn.",
                    'type': 'type_error.invalid'
                }]
            )
        else:
            food_in_query.update({"inventory": inventory_limit}, synchronize_session=False)

        new_food_out = FoodOut(
            food_in_id=food_out_data.food_in_id,
            quantity=food_out_data.quantity,
            inventory=inventory_limit,
            pond_id=food_out_data.pond_id,
            in_date=food_out_data.in_date,
            note=food_out_data.note
        )
        self.db.add(new_food_out)
        self.db.commit()
        self.db.refresh(new_food_out)

        return new_food_out


    def get_all(self, food_filter_data: FoodOutFilter, all = False):
        query = self.db.query(FoodOut).join(FoodIn, FoodIn.id == FoodOut.food_in_id)

        if food_filter_data.food_id:
            query = query.filter(FoodIn.food_id == food_filter_data.food_id)

        if food_filter_data.adopt_area_id:
            query = query.filter(FoodIn.adopt_area_id == food_filter_data.adopt_area_id)

        if food_filter_data.food_in_id:
            query = query.filter(FoodOut.food_in_id == food_filter_data.food_in_id)

        if food_filter_data.pond_id:
            query = query.filter(FoodOut.pond_id == food_filter_data.pond_id)

        query = query.order_by(desc(FoodOut.created_at))

        if all == False:
            if food_filter_data.limit:
                query = query.limit(food_filter_data.limit)

            if food_filter_data.offset:
                query = query.offset(food_filter_data.offset)
                
        return query.all()

    def get_total_quantity_food_out_for_pond(self, pond_id: int):
        food_out = self.db.query(FoodOut).filter(FoodOut.pond_id == pond_id).all()

        total_quantity = 0
        for i in food_out:
            total_quantity += i.quantity

        return total_quantity


    def get_food_out_history(self, pond_id: int):
        food_out_history_date = self.db.query(cast(FoodOut.created_at, Date).label("in_date"))\
                                            .filter(FoodOut.pond_id == pond_id)\
                                            .order_by(desc("in_date")).distinct().all()
                                            

        food_outs = self.db.query(FoodOut).filter(FoodOut.pond_id == pond_id).all()

        food_out_history_datas = []

        for i in food_out_history_date:
            food_out_data = []
            for j in food_outs:
                if str(i.in_date) == str(j.created_at.date()):
                    if j.food_in.food.supplier:
                        food_name = f'{j.food_in.food.name}{" "}{j.food_in.food.supplier.name}{" - "}{j.food_in.type_code}{"ly"}'
                    else:
                        food_name = f'{j.food_in.food.name}{" - "}{j.food_in.type_code}{"ly"}'

                    food_out_data.append(FoodOutHistoryValue(id=j.id, name=food_name, batch_code=j.food_in.batch_code, quantity=j.quantity, note=j.note, in_date=j.created_at))

            food_out_history_datas.append(FoodOutHistoryResponse(in_date=i.in_date, history_datas=food_out_data))

        return food_out_history_datas

