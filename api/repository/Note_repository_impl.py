import logging

from sqlalchemy.exc import MultipleResultsFound

from .INote_repository import IRepository
from api.repository.config.Configuration import Initializer
from .entity.Entity import Note_entity
from .exception.Repository_exception import NoteAlreadyExistsException, NoteNotFoundException, DuplicatedNoteException
from sqlalchemy import exists, select
from datetime import datetime
from .entity.Entity import Base

class Repository(IRepository):

    logger = logging.getLogger("task_repository")

    def __init__(self, configuration: Initializer):
        super().__init__(configuration)
        configuration.create_tables(Base)

    
    def save_note(self, note: Note_entity) -> None:
        db = self._db_config.get_session()
        exists_note = self.__exists_by_criteria(db, Note_entity.title == note.title, Note_entity.deadline_date == None)

        if exists_note:
            raise NoteAlreadyExistsException(note.title)
        
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

    def set_completed(self, id: int) -> bool:
        db = self._db_config.get_session()

        exists_note = self.__exists_by_criteria(db, Note_entity.id == id)
        if not exists_note:
            raise NoteNotFoundException(id)
        
        note = db.query(Note_entity).filter_by(id = id).one()
        note.completed = True
        note.deadline_date = datetime.now()

        db.add(note)
        db.commit()
        db.refresh(note)
        db.close()

        return True
        
    def get_expired_notes(self) -> list:
        db = self._db_config.get_session()
        return db.query(Note_entity).filter(Note_entity.completed == True,
            Note_entity.deadline_date < datetime.now()).all()

    def modify(self, note: Note_entity) -> None:
        db = self._db_config.get_session()

        current_note = db.query(Note_entity).filter_by(id = note.id).one_or_none()
        if current_note is None:
            raise NoteNotFoundException(note.id)
        
        updatable_fields = ['title', 'content', 'completed', 'deadline_date', 'updated_date']

        for field in updatable_fields:
            if hasattr(note, field):
                setattr(current_note, field, getattr(note, field))
        
        db.commit()
        db.close()
    
    def remove(self, id: int) -> None:
        # TODO: Implement method
        pass
        
    def __exists_by_criteria(self, db, *criteria) -> bool | None:
        return db.scalar(select(exists().where(*criteria)))

