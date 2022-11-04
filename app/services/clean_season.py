from datetime import datetime
from app.core.service import BaseService
from app.models.base_season_pond import BaseSeasonPonds
from fastapi import HTTPException, status
from app.schemas.clean_season import CleanSeasonCreateRequest, CleanSeasonUpdateRequest
from app.models.clean_season import CleanSeasons


class CleanSeasonsService(BaseService):

    def get_by_id(self, id:int):
        clean_season = self.db.query(CleanSeasons).filter(CleanSeasons.id == id).first()

        if not clean_season:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Clean season id: {id} does not exist",
                            'code': 'ER0017'
                        }]
                )

        return clean_season

    def update_clean_season(self, id: int, clean_season_update_data: CleanSeasonUpdateRequest):
        clean_season = self.get_by_id(id)
        clean_season_query = self.db.query(CleanSeasons).filter(CleanSeasons.id == id)

        if clean_season_update_data.start_date:
            clean_season_query.update({"start_date": clean_season_update_data.start_date}, synchronize_session=False)

        if clean_season_update_data.finish_date:
            clean_season_query.update({"finish_date": clean_season_update_data.finish_date}, synchronize_session=False)

        if clean_season_update_data.process_description:
            clean_season_query.update({"process_description": clean_season_update_data.process_description}, synchronize_session=False)

        if clean_season_update_data.chemical_used:
            clean_season_query.update({"chemical_used": clean_season_update_data.chemical_used}, synchronize_session=False)

        if clean_season_update_data.time_between_season:
            clean_season_query.update({"time_between_season": clean_season_update_data.time_between_season}, synchronize_session=False)

        if clean_season_update_data.time_clear_pond:
            clean_season_query.update({"time_clear_pond": clean_season_update_data.time_clear_pond}, synchronize_session=False)

        self.db.commit()

        return clean_season

    def get_clean_season_by_base_season_id(self, base_season_id: int):
        clean_season = self.db.query(CleanSeasons).join(CleanSeasons.base_season)

        base_season = self.db.query(BaseSeasonPonds).filter(BaseSeasonPonds.id == base_season_id).first()

        if not base_season:
            raise HTTPException(
                         status.HTTP_422_UNPROCESSABLE_ENTITY,
                        [{
                            'base_season': f"Vụ nuôi không tồn tại.",
                            'type': 'type_error.invalid'
                        }]
                     )
        
        clean_season = clean_season.filter(CleanSeasons.base_season_id == base_season_id)

        return clean_season.first()

