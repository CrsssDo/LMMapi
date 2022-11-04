from datetime import datetime
from app.core.service import BaseService
from sqlalchemy import and_
from app.models.address import AddressLevel1
from fastapi import HTTPException, status, Response
from app.models.purchasing_dealer import PurchasingDealers
from app.schemas.purchasing_dealer import PurchasingDealerCreateRequest, PurchasingDealerUpdateRequest
from app.models.collect_season import CollectSeasons
from app.models.base_season_pond import BaseSeasonPonds


class PurchasingDealersService(BaseService):

    def get_by_id(self, id:int):
        purchasing_dealer = self.db.query(PurchasingDealers).filter(PurchasingDealers.id == id).first()

        if not purchasing_dealer:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Purchasing dealer with id: {id} does not exist",
                            'code': 'ER0049'
                        }]
                )
        return purchasing_dealer


    def create(self, purchasing_dealer_data: PurchasingDealerCreateRequest):
        purchasing_code = self.db.query(PurchasingDealers).filter(PurchasingDealers.code == purchasing_dealer_data.code).first()

        if purchasing_code:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Mã cơ sở thu mua đã được sử dụng",
                            'code': 'ER0050'
                        }]
                )

        address_level_1 = self.db.query(AddressLevel1).filter(AddressLevel1.id == purchasing_dealer_data.address_level_1_id).first()

        if not address_level_1:
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Địa chỉ không tồn lại",
        )

        code = purchasing_dealer_data.code

        max_id = self.db.execute("""
                select max(id) from purchasing_dealers 
                """).first()
        if not max_id.max:
            generate = 1
        else:
            generate = max_id.max + 1

        if not code:
            prefix = 'CSTM-'
            if generate < 10:
                code = f'{prefix}{0}{0}{0}{generate}'
            elif generate >= 10 and generate < 100:
                code = f'{prefix}{0}{0}{generate}'
            else:
                code = f'{prefix}{0}{generate}'

        new_purchasing = PurchasingDealers(
            name=purchasing_dealer_data.name,
            code=code,
            address=purchasing_dealer_data.address,
            address_level_1_id=purchasing_dealer_data.address_level_1_id
        )
        self.db.add(new_purchasing)
        self.db.commit()
        self.db.refresh(new_purchasing)

        return new_purchasing


    def get_all(self):
        purchasing_dealers = self.db.query(PurchasingDealers)

        purchasing_dealers = purchasing_dealers.filter(PurchasingDealers.deleted_at.is_(None))

        return purchasing_dealers.order_by(PurchasingDealers.name).all()

    def update_purchasing_dealer(self, id:int, purchasing_dealer_data: PurchasingDealerUpdateRequest):
        purchasing_dealer = self.get_by_id(id)
        purchasing_update = self.db.query(PurchasingDealers).filter(PurchasingDealers.id == id)

        if purchasing_dealer_data.name:
            purchasing_update.update({"name": purchasing_dealer_data.name}, synchronize_session=False)

        if purchasing_dealer_data.address:
            purchasing_update.update({"address": purchasing_dealer_data.address}, synchronize_session=False)

        if purchasing_dealer_data.address_level_1_id:
            purchasing_update.update({"address_level_1_id": purchasing_dealer_data.address_level_1_id}, synchronize_session=False)

        self.db.commit()

        return purchasing_dealer

    def soft_delete_dealers(self, id: int):
        self.get_by_id(id)
        current_time = datetime.now()

        dealer_in_base_season = self.db.query(CollectSeasons).join(CollectSeasons.base_season).filter(and_(CollectSeasons.purchasing_dealer_id == id, BaseSeasonPonds.status.not_in(['Kết thúc','Đã hủy']))).all()

        if dealer_in_base_season:
            raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    [{
                            'error' : True,
                            'message': f"Cơ sở thua mua đang dùng trong vụ nuôi",
                            'code': 'ER0051'
                        }]
                )

        self.db.query(PurchasingDealers).filter(PurchasingDealers.id == id).update({"deleted_at": current_time}, synchronize_session=False)

        self.db.commit()






    
