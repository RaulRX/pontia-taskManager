import logging

from sqlalchemy.exc import MultipleResultsFound

from src.taskmanager.repository.INote_repository import IRepository
from src.taskmanager.infrastructure.Configuration import Initializer
from src.taskmanager.infrastructure.Entity import Note_entity, Base
from src.taskmanager.repository.Repository_exception import NoteNotFoundException, DuplicatedNoteException
from sqlalchemy import exists, select
from datetime import datetime

class Repository(IRepository):

    logger = logging.getLogger("task_repository")

    def __init__(self, configuration: Initializer):
        super().__init__(configuration)
        configuration.create_tables(Base)


    def save_note(self, note: Note_entity) -> None:
        db = self._db_config.get_session()

        db.add(note)
        db.commit()
        db.refresh(note)
        db.close()

    def get_by_id(self, id: int) -> Note_entity:
        db = self._db_config.get_session()
        exists_note = self.__exists_by_criteria(db, Note_entity.id == id)

        if not exists_note:
            raise NoteNotFoundException(id)

        try:
            row = db.query(Note_entity).filter_by(id = id).one()
            db.close()

            return row

        except MultipleResultsFound:
            raise DuplicatedNoteException(id)
        
    def exists_by_id(self, id: int | None) -> bool:
        db = self._db_config.get_session()
        
        exists = self.__exists_by_criteria(db, Note_entity.id == id)
        db.close()

        return exists
    
    def get_all(self) -> list[Note_entity]:
        db = self._db_config.get_session()
        return db.query(Note_entity).all()

    def set_completed(self, id: int) -> bool:
        db = self._db_config.get_session()

        exists_note = self.__exists_by_criteria(db, Note_entity.id == id)
        if not exists_note:
            raise NoteNotFoundException(id)

        note = db.query(Note_entity).filter_by(id = id).one()
        note.completed = True

        db.add(note)
        db.commit()
        db.refresh(note)
        db.close()

        return True

    def get_expired_notes(self) -> list:
        db = self._db_config.get_session()
        return db.query(Note_entity).filter(Note_entity.deadline_date < datetime.now()).all()

    def modify(self, note: Note_entity) -> Note_entity:
        db = self._db_config.get_session()

        current_note = db.query(Note_entity).filter_by(id = note.id).one_or_none()
        if current_note is None:
            raise NoteNotFoundException(note.id)

        if note.title is not None:
            current_note.title = note.title
        if note.content is not None:
            current_note.content += note.content
        if note.completed is not None:
            current_note.completed = note.completed
        if note.deadline_date is not None:
            current_note.deadline_date = note.deadline_date

        db.commit()
        db.refresh(current_note)
        db.close()

        return current_note

    def remove(self, id: int) -> bool:
        db = self._db_config.get_session()

        exists = self.__exists_by_criteria(db, Note_entity.id == id)
        if not exists:
            self.logger.info("Does not exists notes to remove")
            return False
        
        else:
            db.query(Note_entity).filter_by(id = id).delete(synchronize_session=False)
            db.commit()
            db.close()

            return True        

    def remove_all(self) -> bool:
        db = self._db_config.get_session()

        if not self.__exists_at_least_one(db):
            self.logger.info("Does not exists notes to remove")
            return False
        
        note_list = db.query(Note_entity).all()
        for note in note_list:
            db.query(Note_entity).filter_by(id = note.id).delete(synchronize_session=False)
        
        db.commit()
        db.close()

        return True
        

    def __exists_by_criteria(self, db, *criteria) -> bool:
        return db.scalar(select(exists().where(*criteria))) or False
    
    def __exists_at_least_one(self, db) -> bool:
        return db.scalar(select(exists().select_from(Note_entity))) or False

