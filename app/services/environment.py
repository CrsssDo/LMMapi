from app.core.service import BaseService
from app.models.environment import Environments


class EnvironmentsService(BaseService):

    def get_all(self):
        environments = self.db.query(Environments).all()
        return environments
