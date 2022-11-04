from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db
from typing import Callable, Type


class BaseService():
    def __init__(self, db: Session) -> None:
        self.db = db



def get_service(Service: Type[BaseService]) -> Callable:
    def get_repo(db: Session = Depends(get_db)) -> Type[BaseService]:
        return Service(db)
    return get_repo
