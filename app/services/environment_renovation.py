from datetime import date, datetime, timedelta
from sqlalchemy import desc, func, cast, Date
from typing import List
import sqlalchemy as sa
from app.core.service import BaseService
from fastapi import HTTPException, status
from app.models.chemistry import Chemistries
from app.models.environment_renovation import EnvironmentRevovations
from app.models.pond import Ponds
from app.models.unit import Units
from app.schemas.environment_renovation import EnvironmentRenovationCreateRequest, EnvironmentRenovationHistoryResponse, EnvironmentRenovationValue

class EnvironemntRenovationsService(BaseService):

    def get_by_id(self, id: int):
        renovation = self.db.query(EnvironmentRevovations).filter(EnvironmentRevovations.id == id).first()

        if not renovation:
            raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    [{
                            'error' : True,
                            'message': f"Renovation with id: {id} does not exist",
                            'code': 'ER0024'
                        }]
                )
            
        return renovation

    def create(self, renovation_data: EnvironmentRenovationCreateRequest):
        if renovation_data.unit_id:
            unit = self.db.query(Units).filter(Units.id == renovation_data.unit_id).first()

            if not unit:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Đơn vị không tồn tại.",
                )

        if renovation_data.chemistry_id:
            chemistry = self.db.query(Chemistries).filter(Chemistries.id == renovation_data.chemistry_id).first()

            if not chemistry:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Hóa chất không tồn tại.",
                )

        new_renovation = EnvironmentRevovations(
            code=renovation_data.code,
            exp_date=renovation_data.exp_date,
            quantity=renovation_data.quantity,
            pond_id=renovation_data.pond_id,
            unit_id=renovation_data.unit_id,
            chemistry_id=renovation_data.chemistry_id,
            reason=renovation_data.reason
        )
        self.db.add(new_renovation)
        self.db.commit()
        self.db.refresh(new_renovation)

        return new_renovation

    def get_all(self, pond_id: int):
        filter_date = datetime.now().date() - timedelta(days=1)
        renovations = self.db.query(EnvironmentRevovations)

        if pond_id:
            pond = self.db.query(Ponds).filter(Ponds.id == pond_id).first()
            if not pond:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Bể không tồn tại.",
                )

            renovations = renovations.filter(EnvironmentRevovations.pond_id == pond_id)

        renovations = renovations.filter(EnvironmentRevovations.created_at > filter_date)

        return renovations.order_by(desc(EnvironmentRevovations.created_at)).all()


    def update(self, id: int, renovation_data: EnvironmentRenovationCreateRequest):
        renovation = self.get_by_id(id)
        renovation_query = self.db.query(EnvironmentRevovations).filter(EnvironmentRevovations.id == id)

        if renovation_data.code:
            renovation_query.update({"code": renovation_data.code}, synchronize_session=False)

        if renovation_data.exp_date:
            renovation_query.update({"exp_date": renovation_data.exp_date}, synchronize_session=False)
        
        if renovation_data.quantity:
            renovation_query.update({"quantity": renovation_data.quantity}, synchronize_session=False)

        if renovation_data.chemistry_id:
            renovation_query.update({"chemistry_id": renovation_data.chemistry_id}, synchronize_session=False)

        if renovation_data.unit_id:
            renovation_query.update({"unit_id": renovation_data.unit_id}, synchronize_session=False)

        if renovation_data.reason:
            renovation_query.update({"reason": renovation_data.reason}, synchronize_session=False)

        self.db.commit()

        return renovation


    def get_environment_renovation_history(self, pond_id: int):
        filter_date = datetime.now().date()

        renovation_history_date = self.db.query(cast(EnvironmentRevovations.created_at, Date).label("in_date"))\
                                            .filter(EnvironmentRevovations.pond_id == pond_id)\
                                            .filter(EnvironmentRevovations.created_at < filter_date)\
                                            .distinct().all()
                                            

        revonation_histories = self.db.query(EnvironmentRevovations).filter(EnvironmentRevovations.pond_id == pond_id).all()

        renovation_history_datas = []
        renovation_value = []

        for i in renovation_history_date:
            for j in revonation_histories:
                if i.in_date == j.created_at.date():
                    renovation_value.append(EnvironmentRenovationValue(id=j.id, code=j.code, quantity=j.quantity, exp_date=j.exp_date, chemistry=j.chemistry.name, unit=j.unit.code, reason=j.reason))

            renovation_history_datas.append(EnvironmentRenovationHistoryResponse(in_date=i.in_date, histories=renovation_value))

        return renovation_history_datas


    
