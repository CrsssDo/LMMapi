
from app.models.user import User
from app.models.user_history import UserHistory
from app.schemas.user_history import UserHistoryAction
from app.core.service import BaseService


class UserHistoryService(BaseService):
    def add_create(self, user: User, record_type: int, record_id: int):
        new_history = UserHistory(
            by_user_id=user.id,
            record_type=record_type,
            record_id=record_id,
            action=UserHistoryAction.CREATE,
            detail=''
        )
        self.db.add(new_history)
        self.db.flush()
        return new_history

    def add_delete(self, user: User, record_type: int, record_id: int):
        new_history = UserHistory(
            by_user_id=user.id,
            record_type=record_type,
            record_id=record_id,
            action=UserHistoryAction.DELETE,
            detail=''
        )
        self.db.add(new_history)
        self.db.flush()
        return new_history

    def add_update(self, user: User, record_type: int, record_id: int, origin, updated):
        print(origin.description)
        print(updated.description)

        # new_history = UserHistory(
        #     by_user_id=user.id,
        #     record_type=record_type,
        #     record_id=record_id,
        #     action=UserHistoryAction.UPDATE,
        #     detail=''
        # )
        # self.db.add(new_history)
        # self.db.flush()
        # return new_history

    
