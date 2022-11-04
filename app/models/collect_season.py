from sqlalchemy import DATE, DATETIME, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.supplier import Suppliers
from app.models.address import AddressLevel1, AddressLevel2, AddressLevel3


from app.core.database import Base

class CollectSeasons(Base):
    __tablename__ = 'collect_seasons'
    id = Column(Integer, primary_key=True, nullable=False)
    base_season_pond_id = Column(Integer, ForeignKey("base_season_ponds.id"))
    purchasing_dealer_id = Column(Integer, ForeignKey("purchasing_dealers.id"))
    start_date = Column(DATETIME)
    finish_date = Column(DATETIME)
    fish_size = Column(String)
    amount_of_collection = Column(Integer)
    purchasing_address = Column(String)
    purchasing_address_level_1_id = Column(Integer, ForeignKey("address_level_1.id"))
    purchasing_address_level_2_id = Column(Integer, ForeignKey("address_level_2.id"))
    purchasing_address_level_3_id = Column(Integer, ForeignKey("address_level_3.id"))
    purchasing_dealer = relationship("PurchasingDealers", foreign_keys=[purchasing_dealer_id])
    purchasing_address_level_1 = relationship("AddressLevel1", foreign_keys=[purchasing_address_level_1_id])
    purchasing_address_level_2 = relationship("AddressLevel2", foreign_keys=[purchasing_address_level_2_id])
    purchasing_address_level_3 = relationship("AddressLevel3", foreign_keys=[purchasing_address_level_3_id])







