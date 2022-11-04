from datetime import date, datetime

from sqlalchemy import desc
from app.core.service import BaseService
from fastapi import HTTPException, status
from app.models.adopt import AdoptAreas
from app.models.dead_fish_diary import DeadFishDiaries
from app.schemas.dead_fish_diary import DeadFishDiaryUpdateRequest, DeadFishDiaryCreateRequest
from app.models.pond import Ponds


class DeadFishDiariesService(BaseService):

    def get_by_id(self, id: int):
        dead_fish_diary = self.db.query(DeadFishDiaries).filter(DeadFishDiaries.id == id).first()

        if not dead_fish_diary:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Dead fish diary with id: {id} does not exist",
                            'code': 'ER0020'
                        }]
                )
    
        return dead_fish_diary      

    def get_dead_fish_by_pond_id(self, pond_id):
        today = datetime.now().date()
        pond = self.db.query(Ponds).filter(Ponds.id == pond_id).first()
        if not pond:
            raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'pond': f"Bể không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                     )

        dead_fish_diary = self.db.query(DeadFishDiaries).filter(DeadFishDiaries.pond_id == pond_id)\
                        .filter(DeadFishDiaries.in_date == today).first()

        return dead_fish_diary
                            
                            
    def update(self, id: int, dead_fish_update_data: DeadFishDiaryUpdateRequest):
        self.get_by_id(id)
        date_now = datetime.now().date()
        dead_fish_diary_query = self.db.query(DeadFishDiaries).filter(DeadFishDiaries.id == id)

        if dead_fish_diary_query.first().in_date < date_now:
            raise HTTPException(
                         status.HTTP_400_BAD_REQUEST,
                        [{
                            'detail': f"Bạn không được phép cập nhật giá trị ngày hôm trước.",
                            'type': 'type_error.invalid'
                        }]
                    )
        
        if dead_fish_update_data.average_weight:
            dead_fish_diary_query.update({"average_weight": dead_fish_update_data.average_weight}, synchronize_session=False)

        if dead_fish_update_data.quantity:
            if dead_fish_update_data.quantity < 0:
                raise HTTPException(
                         status.HTTP_400_BAD_REQUEST,
                        [{
                            'quantity': f"Số lượng không được nhập số âm.",
                            'type': 'type_error.invalid'
                        }]
                    )

            if dead_fish_update_data.quantity < dead_fish_diary_query.first().quantity:
                raise HTTPException(
                         status.HTTP_400_BAD_REQUEST,
                        [{
                            'quantity': f"Giá trị nhập vào không chính xác.",
                            'type': 'type_error.invalid'
                        }]
                    )

            quantity_cal = dead_fish_update_data.quantity - dead_fish_diary_query.first().quantity

            dead_fish_diary_query.update({"quantity": dead_fish_update_data.quantity}, synchronize_session=False)
            dead_fish_diary_query.update({"accumulated_loss": DeadFishDiaries.accumulated_loss + quantity_cal}, synchronize_session=False)
            dead_fish_diary_query.update({"accumulated_exist": DeadFishDiaries.accumulated_exist - quantity_cal}, synchronize_session=False)
            self.db.flush()
            dead_fish_diary_query.update({"estimated_volume": DeadFishDiaries.accumulated_exist * DeadFishDiaries.average_weight / 1000} )

        if dead_fish_update_data.mass and dead_fish_update_data.quantity:
            if dead_fish_update_data.mass < 0:
                raise HTTPException(
                         status.HTTP_400_BAD_REQUEST,
                        [{
                            'mass': f"Khối lượng không được nhập số âm.",
                            'type': 'type_error.invalid'
                        }]
                    )

            dead_fish_diary_query.update({"mass": dead_fish_update_data.mass}, synchronize_session=False)

        if dead_fish_update_data.health_condition:
            dead_fish_diary_query.update({"health_condition": dead_fish_update_data.health_condition}, synchronize_session=False)

        self.db.commit()      

        return dead_fish_diary_query.first()  


    def get_all(self, adopt_id: int, in_date: date):
        dead_fish_query = self.db.query(DeadFishDiaries).join(DeadFishDiaries.pond)

        if adopt_id:
            adopt = self.db.query(AdoptAreas).filter(AdoptAreas.id == adopt_id).first()

            if not adopt:
                raise HTTPException(
                         status.HTTP_403_FORBIDDEN,
                        [{
                            'adopt': f"Vùng nuôi không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                    )

            dead_fish_query = dead_fish_query.filter(Ponds.adopt_area_id == adopt_id)

        if in_date:
            dead_fish_query = dead_fish_query.filter(DeadFishDiaries.in_date == in_date)

        return dead_fish_query.all()


    def get_dead_fish_diary_history(self, pond_id: int):
        dead_fish_histories = self.db.query(DeadFishDiaries).join(DeadFishDiaries.pond)

        if pond_id:
            pond = self.db.query(Ponds).filter(Ponds.id == pond_id).first()

            if not pond:
                raise HTTPException(
                         status.HTTP_403_FORBIDDEN,
                        [{
                            'adopt': f"Bể không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                    )

            dead_fish_histories = dead_fish_histories.filter(DeadFishDiaries.pond_id == pond_id)

        return dead_fish_histories.order_by(desc(DeadFishDiaries.created_at)).all()


    def get_dead_fish_by_range_date(self, pond_id: int, from_date: date, to_date: date):
        dead_fish_diary = self.db.query(DeadFishDiaries)

        if pond_id:
            dead_fish_diary = dead_fish_diary.filter(DeadFishDiaries.pond_id == pond_id)

        dead_fish_diary = dead_fish_diary.filter(DeadFishDiaries.in_date >= from_date)\
                                                        .filter(DeadFishDiaries.in_date <= to_date)
                                                        


        return dead_fish_diary.all()


        
