import logging

from sqlalchemy.exc import MultipleResultsFound

from api.repository.config.Configuration import Initializer
from .model.Note import Note
from .exception.Exceptions import NoteAlreadyExistsException, NoteNotFoundException, DuplicatedNoteException
from sqlalchemy import exists, select

class Base_repository:

    def __init__(self, db_config: Initializer):
        self.__db_config = db_config

class Repository(Base_repository):

    logger = logging.getLogger("task_repository")

    def __init__(self, configuration: Initializer):
        super().__init__(configuration)

    
    def save_note(self, note: Note) -> None:
        db = self.__db_config.get_session()
        exists_note = self.__exists_by_criteria(Note.title == note.title, Note.completed == False, Note.deadline_date == None)

        if exists_note:
            raise NoteAlreadyExistsException(note.title)
        
        db.add(note)
        db.commit()
        db.refresh(note)
        db.close()

    def get_by_id(self, id: int) -> Note:
        db = self.__db_config.get_session()
        exists_note = self.__exists_by_criteria(Note.id == id)

        if not exists_note:
            raise NoteNotFoundException(id)
        
        try:
            row = db.query(Note).filter_by(id = id).one()
            db.close()

            return row

        except MultipleResultsFound:
            raise DuplicatedNoteException(id)

    def set_completed(self, id: int) -> bool:
        db = self.__db_config.get_session()

        note = self.get_by_id(id)
        note.completed = True

        db.add(note)
        db.commit()
        db.refresh(note)
        db.close()

        return True
        
    def get_expired_notes(self) -> List:
        #TODO
        pass

    def modify(self, note: Note) -> None:
        # TODO
        pass

    def __exists_by_criteria(self, *criteria) -> bool | None:
        db = self.__db_config.get_session()
        return db.scalar(select(exists().where(*criteria)))

