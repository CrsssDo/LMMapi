from datetime import datetime, timedelta
from app.core.service import BaseService
from sqlalchemy import and_, desc
from typing import List
from app.models.base_season import BaseSeasons
from app.models.base_season_pond import BaseSeasonPonds
from app.models.clean_season import CleanSeasons
from app.models.collect_season import CollectSeasons
from app.models.measure_index import MeasureIndexes
from app.models.water_index_season import WaterIndexSeasons
from app.models.pond import Ponds
from app.schemas.base_season import BaseSeasonCreateRequest, BaseSeasonStatus
from fastapi import HTTPException, status, Response
from app.models.history_status_season import HistoryStatusSeasons
from app.schemas.base_season_pond import BaseSeasonPondsStatus
from app.schemas.base_season import BaseSeasonPondResponse, BaseSeasonListResponse


class BaseSeasonsService(BaseService):

    def get_by_id(self, id:int):
        base_season = self.db.query(BaseSeasons).filter(BaseSeasons.id == id).first()

        if not base_season:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Vụ nuôi với id: {id} không tồn tại",
                            'code': 'ER0004'
                        }]
                )
        return base_season


    def create(self, base_season_data: BaseSeasonCreateRequest):
        validate_date = base_season_data.expected_start_date + timedelta(days=60)
        if base_season_data.expected_end_date <= validate_date:
            raise HTTPException(
                        status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'error' : True,
                            'message': f"Ngày dự kiến kết thúc phải lớn hơn bắt đầu ít nhất 60 ngày",
                            'code': 'ER0004'
                        }]
                )

        for pond_id in base_season_data.pond_list:
            pond = self.db.query(Ponds).filter(Ponds.id == pond_id).filter(Ponds.status == False).first()

            if pond:
                raise HTTPException(
                            status.HTTP_422_UNPROCESSABLE_ENTITY,
                            [{
                                'pond': f"Bể {pond.code} không thể sử dụng.",
                                'type': 'type_error.invalid'
                            }]
                        )


        base_season_inprogress = self.db.query(BaseSeasons).filter(and_(BaseSeasons.adopt_area_id == base_season_data.adopt_area_id, BaseSeasons.status.in_(['Mới','Đang nuôi']))).order_by(BaseSeasons.code).all()

        for check in base_season_inprogress:
            if check:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    [{
                            'error' : True,
                            'message': f"Đang trong vụ nuôi {check.code}, không thể tạo vụ nuôi mới",
                            'code': 'ER0005'
                        }]
                )

        measure_indexes = self.db.query(MeasureIndexes).filter(MeasureIndexes.deleted_at.is_(None)).all()


        max_id = self.db.execute("""
                select max(id) from base_seasons 
                """).first()
        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        prefix = 'VNC-'
        if generate < 10:
            code = f'{prefix}{0}{0}{0}{generate}'
        elif generate >= 10 and generate < 100:
            code = f'{prefix}{0}{0}{generate}'
        elif generate >= 100 and generate < 1000:
            code = f'{prefix}{0}{generate}'
        else:
            code = f'{prefix}{generate}'

        new_base_season = BaseSeasons(
            code=code,
            status=BaseSeasonStatus.new,
            notes=base_season_data.notes,
            adopt_area_id=base_season_data.adopt_area_id,
            expected_start_date=base_season_data.expected_start_date,
            expected_end_date=base_season_data.expected_end_date
        )
        self.db.add(new_base_season)
        self.db.flush()

        for pond_id in base_season_data.pond_list:
            new_base_season_pond = BaseSeasonPonds(
                pond_id=pond_id,
                base_season_id=new_base_season.id,
                status=BaseSeasonPondsStatus.waiting
            )
            self.db.add(new_base_season_pond)
            self.db.flush()

            new_collect_season = CollectSeasons(
                base_season_pond_id=new_base_season_pond.id
            )
            self.db.add(new_collect_season)
            self.db.flush()

            new_clean_season = CleanSeasons(
                base_season_pond_id=new_base_season_pond.id
            )
            self.db.add(new_clean_season)
            self.db.flush()

            history_status = HistoryStatusSeasons(
                base_season_pond_id=new_base_season_pond.id,
                status=BaseSeasonPondsStatus.waiting
            )
            self.db.add(history_status)
            self.db.flush()

            for measure_index in measure_indexes:
                new_water_index_season = WaterIndexSeasons(
                    base_season_pond_id=new_base_season_pond.id,
                    measure_index_id=measure_index.id,
                    status=measure_index.status
                )
                self.db.add(new_water_index_season)
                self.db.flush()

            
        self.db.commit()
        self.db.refresh(new_base_season)

        return new_base_season

    def create_pond_season_into_already_exist_base_season(self, id: int, pond_list: List = []):
        base_season = self.get_by_id(id)
        for pond_id in pond_list:
            pond = self.db.query(Ponds).filter(Ponds.id == pond_id).filter(Ponds.status == False).first()

            if pond:
                raise HTTPException(
                            status.HTTP_422_UNPROCESSABLE_ENTITY,
                            [{
                                'pond': f"Bể {pond.code} không thể sử dụng.",
                                'type': 'type_error.invalid'
                            }]
                        )

            pond_in_base_season = self.db.query(BaseSeasons).join(BaseSeasons.base_season_ponds)\
                                                            .filter(BaseSeasons.adopt_area_id == base_season.adopt_area_id)\
                                                            .filter(BaseSeasons.status.not_in(['Đã hủy','Hoàn thành']))\
                                                            .filter(BaseSeasonPonds.status.not_in(['Đã hủy','Kết thúc']))\
                                                            .filter(BaseSeasonPonds.pond_id == pond_id).first()
                                        
            if pond_in_base_season:
                pond_info = self.db.query(Ponds).filter(Ponds.id == pond_id).first()
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"{pond_info.pond_type.name} : {pond_info.pond_type.symbol}{pond_info.number_order} đang trong vụ nuôi"
                    )


        measure_indexes = self.db.query(MeasureIndexes).filter(MeasureIndexes.deleted_at.is_(None)).all()

        for pond_id in pond_list:
            new_base_season_pond = BaseSeasonPonds(
                pond_id=pond_id,
                base_season_id=id,
                status=BaseSeasonPondsStatus.waiting
            )
            self.db.add(new_base_season_pond)
            self.db.flush()

            new_collect_season = CollectSeasons(
                base_season_pond_id=new_base_season_pond.id
            )
            self.db.add(new_collect_season)
            self.db.flush()

            new_clean_season = CleanSeasons(
                base_season_pond_id=new_base_season_pond.id
            )
            self.db.add(new_clean_season)
            self.db.flush()

            history_status = HistoryStatusSeasons(
                base_season_pond_id=new_base_season_pond.id,
                status=BaseSeasonPondsStatus.waiting
            )
            self.db.add(history_status)
            self.db.flush()

            for measure_index in measure_indexes:
                new_water_index_season = WaterIndexSeasons(
                    base_season_pond_id=new_base_season_pond.id,
                    measure_index_id=measure_index.id,
                    status=measure_index.status
                )
                self.db.add(new_water_index_season)
                self.db.flush()

            
        self.db.commit()
        self.db.refresh(base_season)

        return base_season


    def get_all(self, adopt_id: int):
        base_seasons = self.db.query(BaseSeasons)

        if adopt_id:
            base_seasons = base_seasons.filter(BaseSeasons.adopt_area_id == adopt_id)

        base_seasons = base_seasons.order_by(desc(BaseSeasons.created_at)).all()

        list_base_seasons = []
        for base_season in base_seasons:
            pond = []
            for i in base_season.base_season_ponds:
                if i.pond.pond_type:
                    pond_map = f'{i.pond.pond_type.symbol}{i.pond.number_order}'
                else:
                    pond_map = f'{i.pond.code}'
                pond.append(BaseSeasonPondResponse(id=i.id, pond_name=pond_map, status=i.status))
            list_base_seasons.append(BaseSeasonListResponse(id=base_season.id,code=base_season.code,adopt_area_id=base_season.adopt_area_id,status=base_season.status,expected_start_date=base_season.expected_start_date, expected_end_date=base_season.expected_end_date,ponds=pond))

        return list_base_seasons

    def update_status(self, id: int):
        base_season = self.get_by_id(id)

        check_pond_status = self.db.query(BaseSeasons).join(BaseSeasons.base_season_ponds).filter(and_(BaseSeasonPonds.base_season_id == id,BaseSeasonPonds.status.not_in(['Chờ nuôi','Đã hủy']))).all()

        if not check_pond_status:
            self.db.query(BaseSeasons).filter(BaseSeasons.id == id).update({"status": BaseSeasonStatus.cancel}, synchronize_session=False)

            self.db.query(BaseSeasonPonds).filter(BaseSeasonPonds.base_season_id == id).update({"status": BaseSeasonPondsStatus.cancel}, synchronize_session=False)

            self.db.commit()
        else:
            raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    [{
                            'error' : True,
                            'message': f"Hiện tại vẫn còn ao/bể đang trong tiến trình.",
                            'code': 'ER0006'
                        }]
                )          

        return base_season


    def get_processing_bar(self, id):
        base_season = self.get_by_id(id)

        expected_start_date = base_season.expected_start_date.date()
        expected_end_date = base_season.expected_end_date.date()

        current_date = datetime.now().date()

        completed_date = abs(current_date - expected_start_date)

        total_date = abs(expected_end_date - expected_start_date)

        processing_date = (completed_date / total_date) * 100

        processing_date = int(processing_date)

        return processing_date




