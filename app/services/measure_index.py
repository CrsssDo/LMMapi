from datetime import datetime
from sqlalchemy import and_
from typing import Optional
from app.core.service import BaseService
from app.models.measure_index import MeasureIndexes
from app.schemas.measure_index import MeasureIndexCreateRequest, MeasureIndexUpdateStatusRequest
from fastapi import HTTPException, status
from app.models.water_diary import WaterDiaries
from app.models.water_diary_detail import WaterDiariesDetail
from app.models.water_index_season import WaterIndexSeasons
from app.models.base_season_pond import BaseSeasonPonds
from app.models.base_season import BaseSeasons
from app.models.unit import Units


class MeasureIndexesService(BaseService):

    def get_by_id(self, id:int):
        unit = self.db.query(MeasureIndexes).filter(MeasureIndexes.id == id).first()

        if not unit:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Measure with id: {id} does not exist",
                            'code': 'ER0039'
                        }]
                )
        return unit


    def create(self, measure_data:MeasureIndexCreateRequest):
        measure_index = self.db.query(MeasureIndexes).filter(and_(MeasureIndexes.code == measure_data.code, MeasureIndexes.deleted_at.is_(None))).first()

        if measure_index:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0040'
                        }]
                )

        if measure_data.max_range and measure_data.min_range:
            if measure_data.max_range <= measure_data.min_range:
                raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'range': f"Ngưỡng trên phải lớn hơn ngưỡng dưới.",
                            'type': 'type_error.invalid'
                        }]
                     )

        new_measure_index = MeasureIndexes(**measure_data.dict())
        self.db.add(new_measure_index)
        self.db.commit()
        self.db.refresh(new_measure_index)

        return new_measure_index


    def get_all(self, measure_status: Optional[bool] = False):
        measure_indexes = self.db.query(MeasureIndexes)

        if measure_status == True:
            measure_indexes = measure_indexes.filter(MeasureIndexes.status == measure_status)

        measure_indexes = measure_indexes.filter(MeasureIndexes.deleted_at.is_(None))

        return measure_indexes.order_by(MeasureIndexes.code).all()

    def update_measure_index(self, id:int, measure_data: MeasureIndexCreateRequest):
        measure_index = self.get_by_id(id)
        measure_index_query = self.db.query(MeasureIndexes)
        measure_index_update = measure_index_query.filter(MeasureIndexes.id == id)

        if measure_data.code and measure_index.code != measure_data.code:
            measure_code = measure_index_query.filter(and_(MeasureIndexes.code == measure_data.code, MeasureIndexes.deleted_at.is_(None))).first()
            if measure_code:
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Dữ liệu đã tồn tại",
                            'code': 'ER0040'
                        }]
                )
                   
            measure_index_update.update({"code": measure_data.code})

        if measure_data.max_range and measure_data.min_range:
            if measure_data.max_range <= measure_data.min_range:
                raise HTTPException(
                        status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'range': f"Ngưỡng trên phải lớn hơn ngưỡng dưới.",
                            'type': 'type_error.invalid'
                        }]
                    )
            measure_index_update.update({
                "max_range": measure_data.max_range,
                "min_range": measure_data.min_range
            })
        
        if measure_data.water_environment:
            measure_index_update.update({"water_environment": measure_data.water_environment})

        if measure_data.unit_id:
            unit_deleted = self.db.query(Units).filter(and_(Units.id == measure_data.unit_id, Units.deleted_at.is_not(None))).first()

            if unit_deleted:
                raise HTTPException(
                        status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'toast': f"Đơn vị đã bị xóa.",
                            'type': 'type_error.invalid'
                        }]
                    )

        measure_index_update.update({"unit_id": measure_data.unit_id})

        self.db.commit()

        return measure_index

    def update_status(self, id: int, status: MeasureIndexUpdateStatusRequest):
        measure_index = self.get_by_id(id)

        self.db.query(WaterDiariesDetail).filter(WaterDiariesDetail.measure_index_id == id).update({"status": status.status})
        self.db.query(WaterIndexSeasons).filter(WaterIndexSeasons.measure_index_id == id).update({"status": status.status})
        self.db.query(MeasureIndexes).filter(MeasureIndexes.id == id).update(status.dict())
        self.db.commit()
        
        return measure_index


    def delete_measure_index(self, id:int):
        self.get_by_id(id)
        self.db.query(MeasureIndexes).filter(MeasureIndexes.id == id).delete(synchronize_session=False)

        self.db.commit()


    def soft_delete_measure_index(self, id: int):
        self.get_by_id(id)        
        current_time = datetime.now()

        check_base_season = self.db.query(MeasureIndexes).join(WaterIndexSeasons, WaterIndexSeasons.measure_index_id == MeasureIndexes.id)\
                                                        .join(BaseSeasonPonds, BaseSeasonPonds.id == WaterIndexSeasons.base_season_pond_id)\
                                                        .join(BaseSeasons, BaseSeasons.id == BaseSeasonPonds.base_season_id)\
                                                        .filter(and_(MeasureIndexes.id == id, BaseSeasons.status.not_in(["Kết thúc","Đã hủy"]))).all()

        if check_base_season:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Chỉ số hiện tại đang dùng trong vụ nuôi.",
                            'code': 'ER0061'
                        }]
                )

        measure_index_in_check_diary = self.db.query(MeasureIndexes).join(WaterDiariesDetail, MeasureIndexes.id == WaterDiariesDetail.measure_index_id)\
                                                .join(WaterDiaries, WaterDiaries.id == WaterDiariesDetail.water_diaries_id).\
                                                filter(and_(WaterDiariesDetail.measure_index_id == id,  WaterDiaries.in_date == current_time.date())).all()

        if measure_index_in_check_diary:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Chỉ số hiện tại đang dùng trong kiểm tra nước hằng ngày.",
                            'code': 'ER062'
                        }]
                )

        self.db.query(MeasureIndexes).filter(MeasureIndexes.id == id).delete(synchronize_session=False)

        self.db.commit()






    
