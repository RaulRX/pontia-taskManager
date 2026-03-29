from abc import ABC, abstractmethod
from src.taskmanager.infrastructure.Configuration import Db_initializer
from src.taskmanager.infrastructure.Entity import Note_entity
import logging
class Base_repository:

    def __init__(self, db_config):
        self._db_config = db_config

class IRepository(ABC, Base_repository):

    logger = logging.getLogger("note_repository")

    @abstractmethod
    def save_note(self, note: Note_entity) -> None:
        raise NotImplementedError("Interface method 'save_note' must be implemented by another class")

    @abstractmethod
    def get_all(self) -> list[Note_entity]:
        raise NotImplementedError("Interface method 'get_all' must be implemented by another class")

    @abstractmethod
    def get_by_id(self, id: (int | None)) -> Note_entity:
        raise NotImplementedError("Interface method 'get_by_id' must be implemented by another class")
    
    @abstractmethod
    def exists_by_id(self, id: int | None) -> bool:
        raise NotImplementedError("Interface method 'exists_by_id' must be implemented by another class")
    
    @abstractmethod
    def set_completed(self, id: int | None, completed: bool) -> bool:
        raise NotImplementedError("Interface method 'set_completed' must be implemented by another class")

    @abstractmethod
    def get_expired_notes(self) -> list:
        raise NotImplementedError("Interface method 'get_expired_notes' must be implemented by another class")

    @abstractmethod
    def modify(self, note: Note_entity) -> Note_entity:
        raise NotImplementedError("Interface method 'modify' must be implemented by another class")

    @abstractmethod
    def remove(self, id: int) -> bool:
        raise NotImplementedError("Interface method 'remove' must be implemented by another class")
    
    @abstractmethod
    def remove_all(self) -> bool:
        raise NotImplementedError("Interface method 'remove_all_notes' must be implemented by another class")
