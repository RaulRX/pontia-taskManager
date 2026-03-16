from abc import ABC, abstractmethod
from .entity.Entity import Note_entity
from api.repository.config.Configuration import Initializer

class Base_repository:

    def __init__(self, db_config: Initializer):
        self._db_config = db_config

class IRepository(ABC, Base_repository):

    @abstractmethod
    def save_note(self, note: Note_entity) -> None:
        raise NotImplementedError("Interface method 'save_note' must be implemented by another class")

    @abstractmethod
    def get_by_id(self, id: int) -> Note_entity:
        raise NotImplementedError("Interface method 'get_by_id' must be implemented by another class")

    @abstractmethod
    def set_completed(self, id: int) -> bool:
        raise NotImplementedError("Interface method 'set_completed' must be implemented by another class")
        
    @abstractmethod
    def get_expired_notes(self) -> list:
        raise NotImplementedError("Interface method 'get_expired_notes' must be implemented by another class")
        
    @abstractmethod
    def modify(self, note: Note_entity) -> None:
        raise NotImplementedError("Interface method 'modify' must be implemented by another class")

    @abstractmethod
    def remove(self, id: int) -> None:
        raise NotImplementedError("Interface method 'remove' must be implemented by another class")