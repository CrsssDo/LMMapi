from datetime import datetime
from sqlalchemy import and_
from sqlalchemy import desc
from app.core.service import BaseService
from app.models.address import AddressLevel1
from app.models.base_season_pond import BaseSeasonPonds
from app.models.dead_fish_diary import DeadFishDiaries
from app.models.base_season import BaseSeasons
from app.models.pond import Ponds
from app.models.supplier import Suppliers
from app.schemas.base_season import BaseSeasonStatus
from app.schemas.base_season_pond import BaseSeasonPondCreateRequest, BaseSeasonPondsUpdateRequest, BaseSeasonPondsStatus, BaseSeasonUpdateStatusRequest
from app.models.fish_original import OriginalFishes
from fastapi import HTTPException, status, Response
from app.schemas.base_season_pond import BaseSeasonPondsStatus
from app.models.purchasing_dealer import PurchasingDealers
from app.models.history_status_season import HistoryStatusSeasons


class BaseSeasonPondsService(BaseService):

    def get_by_id(self, id:int):
        base_season = self.db.query(BaseSeasonPonds).filter(BaseSeasonPonds.id == id).first()

        if not base_season:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Vụ nuôi với id: {id} không tồn tại",
                            'code': 'ER0003'
                        }]
                )

        return base_season

    def update_pond_base_season(self, id: int, base_season_update_data: BaseSeasonPondsUpdateRequest):
        base_season = self.get_by_id(id)
        base_season_query = self.db.query(BaseSeasonPonds).filter(BaseSeasonPonds.id == id)

        if base_season_update_data.origin_fish_id:
            origin_fish = self.db.query(OriginalFishes).filter(OriginalFishes.id == base_season_update_data.origin_fish_id).first()
            if not origin_fish:
                raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'origin_fish': f"Cá giống không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                     )

            base_season_query.update({"origin_fish_id": base_season_update_data.origin_fish_id}, synchronize_session=False)


        if base_season_update_data.supplier_id:
            supplier = self.db.query(Suppliers).filter(Suppliers.id == base_season_update_data.supplier_id).first()
            if not supplier:
                raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'pond': f"Nhà cung cấp không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                     )

            base_season_query.update({"supplier_id": base_season_update_data.supplier_id}, synchronize_session=False)
            
        
        
        if base_season_update_data.supplier_address:
            base_season_query.update({"supplier_address": base_season_update_data.supplier_address}, synchronize_session=False)

        if base_season_update_data.supplier_address_level_3_id:
            base_season_query.update({"supplier_address_level_1_id": base_season_update_data.supplier_address_level_1_id}, synchronize_session=False)

            base_season_query.update({"supplier_address_level_2_id": base_season_update_data.supplier_address_level_2_id}, synchronize_session=False)

            base_season_query.update({"supplier_address_level_3_id": base_season_update_data.supplier_address_level_3_id}, synchronize_session=False)

        if base_season_update_data.note:
            base_season_query.update({"note": base_season_update_data.note}, synchronize_session=False)

        if base_season_update_data.in_date:
            base_season_query.update({"in_date": base_season_update_data.in_date}, synchronize_session=False)

        if base_season_update_data.quantity:
            base_season_query.update({"quantity": base_season_update_data.quantity}, synchronize_session=False)

        if base_season_update_data.density:
            base_season_query.update({"density": base_season_update_data.density}, synchronize_session=False)

        if base_season_update_data.amount_of_quantity:
            base_season_query.update({"amount_of_quantity": base_season_update_data.amount_of_quantity * 1000}, synchronize_session=False)
        
        if base_season_update_data.comment:
            base_season_query.update({"comment": base_season_update_data.comment}, synchronize_session=False)

        if base_season_update_data.reason_cancel:
            base_season_query.update({"reason_cancel": base_season_update_data.reason_cancel}, synchronize_session=False)

        self.db.commit()

        return base_season


    def update_status(self, id:int, base_season_status: str):
        base_season_pond = self.get_by_id(id)
        nextStatusList = {
            "Chờ nuôi" : [('Đang nuôi'),('Đã hủy')],
            "Đang nuôi" : [('Đang thu hoạch')],
            "Đang thu hoạch" : [('Đã thu hoạch')],
            "Đã thu hoạch" : [('Đang vệ sinh'),('Đã kiểm tra')],
            "Đang vệ sinh" : [('Đã vệ sinh'),('Đã kiểm tra')],
            "Đã vệ sinh" : [('Đang kiểm tra'),('Đã kiểm tra')],
            "Đang kiểm tra" : [('Đã kiểm tra')],
            "Đã kiểm tra" : [('Kết thúc')]
            }

        if base_season_status not in nextStatusList[base_season_pond.status]:
            raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'base_season': f"Trạng thái vụ nuôi hiện tại không được phép cập nhật.",
                            'type': 'type_error.invalid'
                        }]
                    )

        self.db.query(BaseSeasonPonds).filter(BaseSeasonPonds.id == id).update({"status": base_season_status}, synchronize_session=False)
        self.db.flush()

        if base_season_status == 'Đang nuôi':
            base_season_query = self.db.query(BaseSeasons)
            base_season_used = base_season_query.join(BaseSeasons.base_season_ponds).filter(BaseSeasonPonds.id == id).first()

            base_season_query.filter(BaseSeasons.id == base_season_used.id).update({"status": BaseSeasonStatus.activating}, synchronize_session=False)

        if base_season_status in ['Kết thúc','Đã hủy']:
            base_season_query = self.db.query(BaseSeasonPonds)

            base_season_detail = base_season_query.filter(BaseSeasonPonds.base_season_id == base_season_pond.base_season_id)

            check_completed = base_season_detail.filter(BaseSeasonPonds.status.not_in(['Kết thúc','Đã hủy'])).all()

            if not check_completed:
                self.db.query(BaseSeasons).filter(BaseSeasons.id == base_season_pond.base_season_id).update({"status": BaseSeasonStatus.completed}, synchronize_session=False)

            if base_season_status == 'Đã hủy':
                check_pond_cancel = base_season_detail.filter(BaseSeasonPonds.status != 'Đã hủy').all()

                if not check_pond_cancel:
                    self.db.query(BaseSeasons).filter(BaseSeasons.id == base_season_pond.base_season_id).update({"status": BaseSeasonStatus.cancel}, synchronize_session=False)

        history_status = HistoryStatusSeasons(
            base_season_pond_id=id,
            status=base_season_status
        )
        self.db.add(history_status)

        if base_season_status in ['Đang nuôi','Đang thu hoạch','Đã thu hoạch','Đang vệ sinh','Đã vệ sinh']:
            date_now = datetime.now().date()
            average_weight = round(base_season_pond.amount_of_quantity / base_season_pond.quantity, 4)
            estimated_volume=base_season_pond.amount_of_quantity / 1000

            dead_fish_diary = self.db.query(DeadFishDiaries).filter(DeadFishDiaries.in_date == date_now)\
                                    .filter(DeadFishDiaries.pond_id == base_season_pond.pond_id).first()

            if not dead_fish_diary:
                new_dead_fish_diary = DeadFishDiaries(
                            pond_id=base_season_pond.pond_id,
                            quantity=0,
                            mass=0,
                            in_date=date_now,
                            average_weight=average_weight,
                            accumulated_loss=0,
                            accumulated_exist=base_season_pond.quantity,
                            estimated_volume=estimated_volume
                        )
                self.db.add(new_dead_fish_diary)
            
        self.db.commit()

        return base_season_pond












            






