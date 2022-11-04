from datetime import datetime
from typing import List
from sqlalchemy import and_, desc
from app.core.service import BaseService
from app.models.water_diary_detail import WaterDiariesDetail
from app.models.water_diary import WaterDiaries
from app.schemas.water_diary_detail import WaterDiaryDetailCreateRequest
from app.schemas.water_diary import WaterDiaryCreateRequest, WaterDiaryFilter, WaterDiaryCommentCreateRequest, WaterDiariesReportResponse, MeasuresReportResponse
from fastapi import HTTPException, status
from app.models.measure_index import MeasureIndexes
from app.models.water_diary_history import WaterDiaryHistories
from app.schemas.water_diary_history import WaterDiaryHistoryResponse
from app.models.adopt import AdoptAreas
from app.utils.generate import generate_code
from app.models.pond import Ponds


class WaterDiariesService(BaseService):

    def get_by_id(self, id: int):
        water_diary = self.db.query(WaterDiaries).filter(WaterDiaries.id == id).first()

        if not water_diary:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Water diary with id: {id} does not exist",
                            'code': 'ER0059'
                        }]
                )
        return water_diary

    def create(self,water_diary_data: WaterDiaryCreateRequest):
        date_now = datetime.now().date()

        pond = self.db.query(Ponds).filter(Ponds.id == water_diary_data.pond_id).first()

        if not pond:
            raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'pond': f"Bể không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                     )

        water_diary = self.db.query(WaterDiaries).filter(WaterDiaries.pond_id == water_diary_data.pond_id)\
                        .filter(WaterDiaries.in_date == date_now).first()
        
        if not water_diary:
            new_water_diaries = WaterDiaries(
                    pond_id=water_diary_data.pond_id,
                    in_date=date_now
                )
            self.db.add(new_water_diaries)
            self.db.flush()

            measure_indexes = self.db.query(MeasureIndexes).filter(MeasureIndexes.deleted_at.is_(None)).order_by(MeasureIndexes.code).all()

            for measure_index in measure_indexes:
                if measure_index.status == True:
                    new_water_diarie_detail = WaterDiariesDetail(
                        water_diaries_id=new_water_diaries.id,
                        measure_index_id=measure_index.id,
                        water_measure_value=None,
                        status=True
                    )
                    new_water_diarie_history = WaterDiaryHistories(
                            water_diary_id=new_water_diaries.id,
                            measure_index_id=measure_index.id,
                            measure_value=None
                        )
                else:
                    new_water_diarie_detail = WaterDiariesDetail(
                        water_diaries_id=new_water_diaries.id,
                        measure_index_id=measure_index.id,
                        water_measure_value=None,
                        status=False
                    )
                    new_water_diarie_history = WaterDiaryHistories(
                            water_diary_id=new_water_diaries.id,
                            measure_index_id=measure_index.id,
                            measure_value=None
                    )
                
                self.db.add(new_water_diarie_history)
                self.db.add(new_water_diarie_detail)

            self.db.commit()

            return new_water_diaries
        else:
            return water_diary


    def update(self, id: int, water_diary_detail_data: List[WaterDiaryDetailCreateRequest], comment_data : WaterDiaryCommentCreateRequest):
        self.get_by_id(id)
        date_now = datetime.now().date()
        water_diary_query = self.db.query(WaterDiaries).filter(WaterDiaries.id == id)

        if water_diary_query.first().in_date < date_now:
            raise HTTPException(
                         status.HTTP_400_BAD_REQUEST,
                        [{
                            'detail': f"Bạn không được phép cập nhật giá trị ngày hôm trước.",
                            'type': 'type_error.invalid'
                        }]
                    )

        exist_water_diaries = self.db.query(WaterDiariesDetail).filter(WaterDiariesDetail.water_diaries_id == id).all()

        out_of_range = False
        water_diary_in_update = self.db.query(WaterDiariesDetail)
        for water_diary in water_diary_detail_data:
            for i in exist_water_diaries:
                if water_diary.measure_index_id == i.measure_index_id:
                    water_diary_in_update.filter(WaterDiariesDetail.id == i.id).update({"water_measure_value": water_diary.water_measure_value})

                    new_water_diarie_history = WaterDiaryHistories(
                            water_diary_id=id,
                            measure_index_id=water_diary.measure_index_id,
                            measure_value=water_diary.water_measure_value
                    )
                    self.db.add(new_water_diarie_history)

                    if i.measure_index.max_range != None and water_diary.water_measure_value > i.measure_index.max_range or\
                        i.measure_index.min_range != None and water_diary.water_measure_value < i.measure_index.min_range:
                            out_of_range = True

        if out_of_range == True:
            if not comment_data.comment:
                raise HTTPException(
                         status.HTTP_400_BAD_REQUEST,
                        [{
                            'detail': f"Chỉ số vượt ngưỡng yêu cầu nhập nhận xét.",
                            'type': 'type_error.invalid'
                        }]
                    )

        water_diary_query.update({"comment": comment_data.comment}, synchronize_session=False)
        self.db.commit()      

        return water_diary_query.first()  


    def get_water_diary_by_pond_id(self, filter_data: WaterDiaryFilter):
        water_diaries = self.db.query(WaterDiaries)
        pond = self.db.query(Ponds).filter(Ponds.id == filter_data.pond_id).first()

        if not pond:
            raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'pond': f"Bể không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                    )

        adopt = self.db.query(AdoptAreas).filter(AdoptAreas.id == filter_data.adopt_id).first()

        if not adopt:
            raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'adopt': f"Vùng nuôi không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                    )

        if filter_data.pond_id:
            water_diaries = water_diaries.join(Ponds).filter(Ponds.adopt_area_id == filter_data.adopt_id)\
                                            .filter(WaterDiaries.pond_id == filter_data.pond_id)

        return water_diaries.all()

    def get_water_history_by_pond_id(self, pond_id: int):
        date_now = datetime.now().date()

        water_histories = self.db.query(WaterDiaryHistories).join(WaterDiaries, WaterDiaries.id == WaterDiaryHistories.water_diary_id)\
                                                            .filter(and_(WaterDiaries.pond_id == pond_id, WaterDiaries.in_date == date_now))\
                                                            .filter(WaterDiaryHistories.measure_value.is_not(None))\
                                                            .order_by(desc(WaterDiaryHistories.updated_at)).all()

        list_water_history = []
        for history in water_histories:
            list_water_history.append(WaterDiaryHistoryResponse(id=history.id, measure_name=history.measure_index.code, measure_value=history.measure_value, in_date=history.updated_at))

        return list_water_history

    def report_water_diaries(self, filter_data: WaterDiaryFilter):
        in_date = datetime.now().date()
        water_diaries_report = self.db.query(WaterDiaries)

        adopt = self.db.query(AdoptAreas).filter(AdoptAreas.id == filter_data.adopt_id).first()

        if not adopt:
            raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'adopt': f"Vùng nuôi không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                    )

        if filter_data.adopt_id:
            water_diaries_report = water_diaries_report.join(Ponds).filter(Ponds.adopt_area_id == filter_data.adopt_id)

        if filter_data.selected_date:
            water_diaries_report = water_diaries_report.filter(WaterDiaries.in_date == filter_data.selected_date)
        else:
            water_diaries_report = water_diaries_report.filter(WaterDiaries.in_date == in_date)

        water_diaries_value = water_diaries_report.order_by(Ponds.code).all()

        report_results = []
        measure_list = []
        for i in water_diaries_value:
            for j in i.water_diaries_value:
                check = False
                if j.measure_index.max_range != None and j.water_measure_value > j.measure_index.max_range:
                    check = True
                if j.measure_index.min_range != None and j.water_measure_value < j.measure_index.min_range:
                    check = True
                measure_list.append(MeasuresReportResponse(id=j.measure_index.id, name=j.measure_index.code, value=j.water_measure_value, is_over=check))

            report_results.append(WaterDiariesReportResponse(pond_code=i.pond.code, pond_id=i.pond.id, measures=measure_list, comment=i.comment))

        return report_results


