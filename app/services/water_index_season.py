from typing import List
from app.core.service import BaseService
from app.schemas.water_index_season import WaterIndexSeasonCreateRequest, WaterIndexSeasonUpdateRequest
from fastapi import HTTPException, status
from app.models.measure_index import MeasureIndexes
from app.models.water_index_season import WaterIndexSeasons
from app.models.base_season_pond import BaseSeasonPonds


class WaterIndexSeasonsService(BaseService):

    def get_by_id(self, id: int):
        water_index_season = self.db.query(WaterIndexSeasons).filter(WaterIndexSeasons.id == id).first()

        if not water_index_season:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Water index season with id: {id} does not exist",
                            'code': 'ER0060'
                        }]
                )
        return water_index_season

    def update(self, base_season_pond_id: int, water_index_season_datas: List[WaterIndexSeasonUpdateRequest], water_index_poison: str = None):
        base_season_query = self.db.query(BaseSeasonPonds).filter(BaseSeasonPonds.id == base_season_pond_id)

        if not base_season_query.first():
            raise HTTPException(
                         status.HTTP_400_BAD_REQUEST,
                        [{
                            'detail': f"Vụ nuôi không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                    )

        exist_water_index_seasons = self.db.query(WaterIndexSeasons).filter(WaterIndexSeasons.base_season_pond_id == base_season_pond_id).all()

        water_diary_in_update = self.db.query(WaterIndexSeasons)
        for water_index in water_index_season_datas:
            for i in exist_water_index_seasons:
                if water_index.measure_index_id == i.measure_index_id:
                    water_diary_in_update.filter(WaterIndexSeasons.id == i.id).update({"water_measure_value": water_index.water_measure_value}, synchronize_session=False)
           
        if water_index_poison:
            base_season_query.update({"water_index_poison": water_index_poison}, synchronize_session=False)


        self.db.commit()      

        return base_season_query.first()

