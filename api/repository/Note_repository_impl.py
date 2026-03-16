import logging

from sqlalchemy.exc import MultipleResultsFound

from .INote_repository import IRepository
from api.repository.config.Configuration import Initializer
from .model.Note import Note
from .exception.Exceptions import NoteAlreadyExistsException, NoteNotFoundException, DuplicatedNoteException
from sqlalchemy import exists, select
from datetime import datetime
from .model.Note import Base

class Repository(IRepository):

    logger = logging.getLogger("task_repository")

    def __init__(self, configuration: Initializer):
        super().__init__(configuration)
        configuration.create_tables(Base)

    
    def save_note(self, note: Note) -> None:
        db = self._db_config.get_session()
        exists_note = self.__exists_by_criteria(db, Note.title == note.title, Note.completed == False, Note.deadline_date == None)

        if exists_note:
            raise NoteAlreadyExistsException(note.title)
        
        db.add(note)
        db.commit()
        db.refresh(note)
        db.close()

    def get_by_id(self, id: int) -> Note:
        db = self._db_config.get_session()
        exists_note = self.__exists_by_criteria(db, Note.id == id)

        if not exists_note:
            raise NoteNotFoundException(id)
        
        try:
            row = db.query(Note).filter_by(id = id).one()
            db.close()

            return row

        except MultipleResultsFound:
            raise DuplicatedNoteException(id)

    def set_completed(self, id: int) -> bool:
        db = self._db_config.get_session()

        note = self.get_by_id(id)
        note.completed = True

        db.add(note)
        db.commit()
        db.refresh(note)
        db.close()

        return True
        
    def get_expired_notes(self) -> list:
        db = self._db_config.get_session()
        return db.query(Note).filter(Note.completed == True or 
                                        Note.deadline_date < datetime.now()).all()

    def modify(self, note: Note) -> None:
        db = self._db_config.get_session()

        current_note = db.query(Note).filter_by(Note.id == note.id).one_or_none()
        if current_note is None:
            raise NoteNotFoundException(f"Note with id {note.id} not found")
        
        updatable_fields = ['title', 'content', 'completed', 'deadline_date', 'updated_date']

        for field in updatable_fields:
            if hasattr(note, field):
                setattr(current_note, field, getattr(note, field))
        
        db.commit()
        db.close()

    def __exists_by_criteria(self, db, *criteria) -> bool | None:
        return db.scalar(select(exists().where(*criteria)))

