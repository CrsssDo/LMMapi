from app.core.service import BaseService
from app.models.address import AddressLevel3, AddressLevel2, AddressLevel1
from app.schemas.address import AddressLevel3Response, AddressLevel2Response, AddressLevel1Response
from fastapi import HTTPException, status, Response


class AddressService(BaseService):

    def get_all_address_lv3(self):
        address_level_3 = self.db.query(AddressLevel3).all()

        return address_level_3


    def get_address_lv2_by_address_lv3_id(self, id: int):
        address_level_2 = self.db.query(AddressLevel2).filter(AddressLevel2.address_level_3_id == id)

        if not address_level_2:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Address level 3 with id: {id} does not exist")


        return address_level_2.all()


    def get_address_lv1_by_address_lv2_id(self, id: int):
        address_level_1 = self.db.query(AddressLevel1).filter(AddressLevel1.address_level_2_id == id).all()

        if not address_level_1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Address level 2 with id: {id} does not exist")


        return address_level_1

    
