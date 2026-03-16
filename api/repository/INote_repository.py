from abc import ABC, abstractmethod
from .model.Note import Note
from api.repository.config.Configuration import Initializer

class Base_repository:

    def __init__(self, db_config: Initializer):
        self._db_config = db_config

class IRepository(ABC, Base_repository):

    @abstractmethod
    def save_note(self, note: Note):
        raise NotImplementedError("Interface method must be implemented by another class")

    @abstractmethod
    def get_by_id(self, id: int) -> Note:
        raise NotImplementedError("Interface method must be implemented by another class")

    @abstractmethod
    def set_completed(self, id: int) -> bool:
        raise NotImplementedError("Interface method must be implemented by another class")
        
    @abstractmethod
    def get_expired_notes(self) -> list:
        raise NotImplementedError("Interface method must be implemented by another class")
        
    @abstractmethod
    def modify(self, note: Note) -> None:
        raise NotImplementedError("Interface method must be implemented by another class")
