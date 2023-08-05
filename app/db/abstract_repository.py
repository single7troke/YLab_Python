import uuid
from abc import ABC, abstractmethod


class AbstractDB(ABC):
    @abstractmethod
    def get_one(self, row_id: str, model):
        pass

    @abstractmethod
    def get_all(self, model):
        pass

    @abstractmethod
    def create(self, model):
        pass

    @abstractmethod
    def update(self, model):
        pass

    @abstractmethod
    def delete(self, model):
        pass
