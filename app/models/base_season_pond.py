from re import U
from sqlalchemy import DATE, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.ext.associationproxy import association_proxy
from app.models.pond import Ponds
from app.models.fish_original import OriginalFishes
from app.models.supplier import Suppliers
from app.models.address import AddressLevel1, AddressLevel2, AddressLevel3
from app.models.history_status_season import HistoryStatusSeasons
from app.models.water_index_season import WaterIndexSeasons


from app.core.database import Base

class BaseSeasonPonds(Base):
    __tablename__ = 'base_season_ponds'
    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String)
    pond_id = Column(Integer, ForeignKey("ponds.id"))
    origin_fish_id = Column(Integer, ForeignKey("original_fishes.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    base_season_id = Column(Integer, ForeignKey("base_seasons.id"))
    status = Column(String)
    in_date = Column(DATE)
    quantity = Column(Integer)
    density = Column(String)
    amount_of_quantity = Column(Integer)
    note = Column(String)
    comment = Column(String)
    water_index_poison = Column(String)
    supplier_address = Column(String)
    supplier_address_level_1_id = Column(Integer, ForeignKey("address_level_1.id"))
    supplier_address_level_2_id = Column(Integer, ForeignKey("address_level_2.id"))
    supplier_address_level_3_id = Column(Integer, ForeignKey("address_level_3.id"))
    reason_cancel = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        onupdate=text('current_timestamp'), nullable=False)
    origin_fish = relationship("OriginalFishes", foreign_keys=[origin_fish_id])
    supplier = relationship("Suppliers", foreign_keys=[supplier_id])
    supplier_address_level_1 = relationship("AddressLevel1", foreign_keys=[supplier_address_level_1_id])
    supplier_address_level_2 = relationship("AddressLevel2", foreign_keys=[supplier_address_level_2_id])
    supplier_address_level_3 = relationship("AddressLevel3", foreign_keys=[supplier_address_level_3_id])
    water_indexes = relationship("WaterIndexSeasons", primaryjoin="BaseSeasonPonds.id==WaterIndexSeasons.base_season_pond_id")
    status_histories = relationship("HistoryStatusSeasons", primaryjoin="BaseSeasonPonds.id==HistoryStatusSeasons.base_season_pond_id")
    clean = relationship("CleanSeasons", primaryjoin="BaseSeasonPonds.id==CleanSeasons.base_season_pond_id", uselist=False)
    collect = relationship("CollectSeasons", primaryjoin="BaseSeasonPonds.id==CollectSeasons.base_season_pond_id", uselist=False)
    pond = relationship("Ponds", primaryjoin="BaseSeasonPonds.pond_id==Ponds.id", uselist=False)









  




