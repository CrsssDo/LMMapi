from datetime import datetime
from app.core.service import BaseService
from app.models.base_season_pond import BaseSeasonPonds
from app.models.fish_original import OriginalFishes
from fastapi import HTTPException, status, Response
from app.schemas.collect_season import CollectSeasonCreateRequest, CollectSeasonUpdateRequest
from app.models.purchasing_dealer import PurchasingDealers
from app.models.collect_season import CollectSeasons


class CollectSeasonsService(BaseService):

    def get_by_id(self, id:int):
        collect_season = self.db.query(CollectSeasons).filter(CollectSeasons.id == id).first()

        if not collect_season:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Collect season id: {id} does not exist",
                            'code': 'ER0019'
                        }]
                )

        return collect_season
        

    def update_collect_season(self, id: int, collect_update_data: CollectSeasonUpdateRequest):
        collect_season = self.get_by_id(id)
        collect_season_query = self.db.query(CollectSeasons).filter(CollectSeasons.id == id)
            
        if collect_update_data.purchasing_dealer_id:
            purchasing_dealer = self.db.query(PurchasingDealers).filter(PurchasingDealers.id == collect_update_data.purchasing_dealer_id).first()
            if not purchasing_dealer:
                raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'pond': f"Cơ sở thu mua không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                    )

            collect_season_query.update({"purchasing_dealer_id": collect_update_data.purchasing_dealer_id}, synchronize_session=False)
        
        if collect_update_data.amount_of_collection:
            collect_season_query.update({"amount_of_collection": collect_update_data.amount_of_collection * 1000}, synchronize_session=False)

        if collect_update_data.fish_size:
            collect_season_query.update({"fish_size": collect_update_data.fish_size}, synchronize_session=False)

        if collect_update_data.start_date:
            collect_season_query.update({"start_date": collect_update_data.start_date}, synchronize_session=False)

        if collect_update_data.finish_date:
            collect_season_query.update({"finish_date": collect_update_data.finish_date}, synchronize_session=False)

        if collect_update_data.purchasing_address:
            collect_season_query.update({"purchasing_address": collect_update_data.purchasing_address}, synchronize_session=False)

        collect_season_query.update({"purchasing_address_level_1_id": collect_update_data.purchasing_address_level_1_id}, synchronize_session=False)
        
        collect_season_query.update({"purchasing_address_level_2_id": collect_update_data.purchasing_address_level_2_id}, synchronize_session=False)

        collect_season_query.update({"purchasing_address_level_3_id": collect_update_data.purchasing_address_level_3_id}, synchronize_session=False)

        self.db.commit()

        return collect_season


    def get_collect_season_by_base_season_id(self, base_season_id: int):
        collect_season = self.db.query(CollectSeasons).join(CollectSeasons.base_season)

        base_season = self.db.query(BaseSeasonPonds).filter(BaseSeasonPonds.id == base_season_id).first()

        if not base_season:
            raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'base_season': f"Vụ nuôi không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                     )
        
        collect_season = collect_season.filter(CollectSeasons.base_season_id == base_season_id)

        return collect_season.first()


        
        
