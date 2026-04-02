from src.taskmanager.infrastructure.data import Query
from src.taskmanager.repository.INote_repository import IRepository
from src.taskmanager.infrastructure.Configuration import Db_initializer
from src.taskmanager.infrastructure.Entity import Note_entity
from src.taskmanager.repository.Repository_exception import NoteNotFoundException, DuplicatedNoteException, MultipleResultsFound
from datetime import datetime

class Repository(IRepository):

    def __init__(self, configuration: Db_initializer):
        super().__init__(configuration)

    def save_note(self, note: Note_entity) -> None:
        self.logger.info("Repository::save_note -> Starting saving note to DB")
        cursor = self._db_config.get_session()

        cursor.execute(Query.INSERT, {
            "title": note.title,
            "content": note.content,
            "completed": note.completed,
            "created_date": datetime.now() if note.created_date is None else note.created_date,
            "updated_date": note.updated_date,
            "deadline_date": note.deadline_date
        })

        self.__commit_and_close_cursor(cursor)
        self.logger.info("Repository::save_note -> Finished saving note to DB")


    def get_by_id(self, id: int) -> Note_entity:
        self.logger.info("Repository::get_by_id -> Starting retrieving note by id from DB")
        cursor = self._db_config.get_session()

        exists_note = self.__exists_by_id(cursor, id)
        if not exists_note:
            self.logger.error(f"Note with id {id} not found")
            raise NoteNotFoundException(id)

        cursor.execute(Query.SELECT_BY_ID, {"id": id})
        result = cursor.fetchone()
        self.__close_cursor(cursor)

        if result is None:
            raise NoteNotFoundException(id)

        self.logger.info("Repository::get_by_id -> Finished retrieving note by id from DB")
        return Note_entity.transform_to_entity(result)

    def exists_by_id(self, id: int | None) -> bool:
        self.logger.info("Repository::exists_by_id -> Starting checking note existence in DB")
        cursor = self._db_config.get_session()

        cursor.execute(Query.EXISTS_BY_ID, {"id": id})
        if cursor.fetchone() is None:
            self.__close_cursor(cursor)
            self.logger.info("Repository::exists_by_id -> Finished checking note existence in DB")
            return False

        self.__close_cursor(cursor)
        self.logger.info("Repository::exists_by_id -> Finished checking note existence in DB")
        return True

    def get_all(self) -> list[Note_entity]:
        self.logger.info("Repository::get_all -> Starting retrieving all notes from DB")
        cursor = self._db_config.get_session()

        exist_any = self.__exists_at_least_one(cursor)
        if not exist_any:
            self.logger.info("Repository::get_all -> Finished retrieving all notes from DB")
            return list()

        cursor.execute(Query.SELECT_ALL)
        all_notes = cursor.fetchall()
        self.__close_cursor(cursor)

        self.logger.info("Repository::get_all -> Finished retrieving all notes from DB")
        return [Note_entity.transform_to_entity(tuple_entity) for tuple_entity in all_notes]

    def set_completed(self, id: int | None, completed: bool) -> bool:
        self.logger.info("Repository::set_completed -> Starting setting note completion in DB")
        cursor = self._db_config.get_session()
        cursor.execute(Query.EXISTS_BY_ID, {"id": id})

        if cursor.fetchone() is None:
            self.logger.error(f"Note with id {id} not found")
            self.__close_cursor(cursor)
            raise NoteNotFoundException(id)

        cursor.execute(Query.SET_COMPLETED, {"id": id, "completed": completed,
                                             "deadline_date": datetime.now() if completed is True else None})

        self.__commit_and_close_cursor(cursor)
        self.logger.info("Repository::set_completed -> Finished setting note completion in DB")
        return True

    def get_expired_notes(self) -> list:
        self.logger.info("Repository::get_expired_notes -> Starting retrieving expired notes from DB")
        cursor = self._db_config.get_session()

        cursor.execute(Query.SELECT_EXPIRED, {"now": datetime.now()})
        all_expired = cursor.fetchall()

        self.__close_cursor(cursor)

        self.logger.info("Repository::get_expired_notes -> Finished retrieving expired notes from DB")
        return [Note_entity.transform_to_entity(tuple_entity) for tuple_entity in all_expired]

    def modify(self, note: Note_entity) -> Note_entity:
        self.logger.info("Repository::modify -> Starting modifying note in DB")
        cursor = self._db_config.get_session()

        exists = self.__exists_by_id(cursor, note.id)
        if not exists:
            self.logger.error(f"Note with id {note.id} not found")
            self.__close_cursor(cursor)
            raise NoteNotFoundException(note.id)

        cursor.execute(Query.UPDATE, {"title": note.title, "content": note.content, "completed": note.completed, "deadline_date":
                                      note.deadline_date, "updated_date": datetime.now(), "id": note.id})
        modified_note = cursor.fetchone()

        self.__commit_and_close_cursor(cursor)

        self.logger.info("Repository::modify -> Finished modifying note in DB")
        return Note_entity.transform_to_entity(modified_note)

    def remove(self, id: int) -> bool:
        self.logger.info("Repository::remove -> Starting removing note from DB")
        cursor = self._db_config.get_session()

        exists = self.__exists_by_id(cursor, id)
        if not exists:
            self.logger.info("Does not exists notes to remove")
            self.__close_cursor(cursor)
            self.logger.info("Repository::remove -> Finished removing note from DB")
            return False

        cursor.execute(Query.DELETE_BY_ID, {"id": id})

        self.__commit_and_close_cursor(cursor)

        self.logger.info("Repository::remove -> Finished removing note from DB")
        return True

    def remove_all(self) -> bool:
        self.logger.info("Repository::remove_all -> Starting removing all notes from DB")
        cursor = self._db_config.get_session()

        if not self.__exists_at_least_one(cursor):
            self.logger.info("Does not exists notes to remove")
            self.__close_cursor(cursor)
            self.logger.info("Repository::remove_all -> Finished removing all notes from DB")
            return False

        cursor.execute(Query.DELETE_ALL)

        self.__commit_and_close_cursor(cursor)

        self.logger.info("Repository::remove_all -> Finished removing all notes from DB")
        return True

    def __commit_and_close_cursor(self, cursor):
        self._db_config.get_connection().commit()
        cursor.close()

    def __close_cursor(self, cursor):
        cursor.close()


    def __exists_by_id(self, cursor, id: int) -> bool:
        cursor.execute(Query.EXISTS_BY_ID, {"id": id})
        return cursor.fetchone()[0]

    def __exists_at_least_one(self, cursor) -> bool:
        cursor.execute(Query.EXISTS_ANY)
        return cursor.fetchone()[0]
