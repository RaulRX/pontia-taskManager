from sqlalchemy import exists, select

from src.taskmanager.repository.INote_repository import IRepository
from src.taskmanager.infrastructure.Configuration import Db_initializer, SqlLite_Initializer
from src.taskmanager.infrastructure.Entity import Note_entity
from src.taskmanager.repository.Repository_exception import NoteNotFoundException, DuplicatedNoteException, MultipleResultsFound
from datetime import datetime

class Repository(IRepository):

    def __init__(self, configuration: Db_initializer):
        super().__init__(configuration)
        configuration.create_tables()


    def save_note(self, note: Note_entity) -> None:
        self.logger.info("Repository::save_note -> Starting saving note to DB")
        db = self._db_config.get_session()

        db.add(note)
        db.commit()
        db.close()
        self.logger.info("Repository::save_note -> Finished saving note to DB")

    def get_by_id(self, id: int) -> Note_entity:
        self.logger.info("Repository::get_by_id -> Starting retrieving note by id from DB")
        db = self._db_config.get_session()
        exists_note = self.__exists_by_criteria(db, Note_entity.id == id)

        if not exists_note:
            self.logger.error(f"Note with id {id} not found")
            raise NoteNotFoundException(id)

        try:
            row = db.query(Note_entity).filter_by(id = id).one()
            db.refresh(row)
            db.close()
            self.logger.info("Repository::get_by_id -> Finished retrieving note by id from DB")
            return row
        except MultipleResultsFound:
            self.logger.error(f"Duplicated note with id {id}")
            raise DuplicatedNoteException(id)

    def exists_by_id(self, id: int | None) -> bool:
        self.logger.info("Repository::exists_by_id -> Starting checking note existence in DB")
        db = self._db_config.get_session()

        exists = self.__exists_by_criteria(db, Note_entity.id == id)
        db.close()

        self.logger.info("Repository::exists_by_id -> Finished checking note existence in DB")
        return exists

    def get_all(self) -> list[Note_entity]:
        self.logger.info("Repository::get_all -> Starting retrieving all notes from DB")
        db = self._db_config.get_session()
        result = db.query(Note_entity).all()
        self.logger.info("Repository::get_all -> Finished retrieving all notes from DB")
        return result

    def set_completed(self, id: int | None, completed: bool) -> bool:
        self.logger.info("Repository::set_completed -> Starting setting note completion in DB")
        db = self._db_config.get_session()
        exists_note = self.__exists_by_criteria(db, Note_entity.id == id)
        if not exists_note:
            self.logger.error(f"Note with id {id} not found")
            raise NoteNotFoundException(id)

        entity_note = db.query(Note_entity).filter_by(id=id).one()
        entity_note.completed = completed
        entity_note.deadline_date = datetime.now() if completed is True else None

        db.commit()
        db.close()

        self.logger.info("Repository::set_completed -> Finished setting note completion in DB")
        return True

    def get_expired_notes(self) -> list:
        self.logger.info("Repository::get_expired_notes -> Starting retrieving expired notes from DB")
        db = self._db_config.get_session()
        result = db.query(Note_entity).filter(Note_entity.deadline_date < datetime.now()).all()
        self.logger.info("Repository::get_expired_notes -> Finished retrieving expired notes from DB")
        return result

    def modify(self, note: Note_entity) -> Note_entity:
        self.logger.info("Repository::modify -> Starting modifying note in DB")
        db = self._db_config.get_session()
        current_note = db.query(Note_entity).filter_by(id = note.id).one_or_none()
        if current_note is None:
            self.logger.error(f"Note with id {note.id} not found")
            raise NoteNotFoundException(note.id)

        if note.title is not None:
            current_note.title = note.title
        if note.content is not None:
            current_note.content = note.content
        if note.completed is not None:
            current_note.completed = note.completed
        if note.deadline_date is not None:
            current_note.deadline_date = note.deadline_date

        db.commit()
        db.refresh(current_note)
        db.close()
        self.logger.info("Repository::modify -> Finished modifying note in DB")
        return current_note

    def remove(self, id: int) -> bool:
        self.logger.info("Repository::remove -> Starting removing note from DB")
        db = self._db_config.get_session()

        exists = self.__exists_by_criteria(db, Note_entity.id == id)
        if not exists:
            self.logger.info("Does not exists notes to remove")
            self.logger.info("Repository::remove -> Finished removing note from DB")
            return False

        else:
            db.query(Note_entity).filter_by(id = id).delete(synchronize_session=False)
            db.commit()
            db.close()

            self.logger.info("Repository::remove -> Finished removing note from DB")
            return True

    def remove_all(self) -> bool:
        self.logger.info("Repository::remove_all -> Starting removing all notes from DB")
        db = self._db_config.get_session()

        if not self.__exists_at_least_one(db):
            self.logger.info("Does not exists notes to remove")
            self.logger.info("Repository::remove_all -> Finished removing all notes from DB")
            return False

        note_list = db.query(Note_entity).all()
        for note in note_list:
            db.query(Note_entity).filter_by(id = note.id).delete(synchronize_session=False)

        db.commit()
        db.close()

        self.logger.info("Repository::remove_all -> Finished removing all notes from DB")
        return True


    def __exists_by_criteria(self, db, *criteria) -> bool:
        return db.scalar(select(exists().where(*criteria))) or False

    def __exists_at_least_one(self, db) -> bool:
        return db.scalar(select(exists().select_from(Note_entity))) or False
