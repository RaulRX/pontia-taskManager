from src.taskmanager.repository.Repository_exception import DuplicatedNoteException, NoteNotFoundException
from src.taskmanager.service.Note_mapper import Mapper
from src.taskmanager.domain.Model import Note
from src.taskmanager.service.Utils import Note_validation
from src.taskmanager.repository.INote_repository import IRepository
from src.taskmanager.service.Service_exception import BadNoteException, DuplicationException, NotFoundException, TextOverflowException, NonWritableException

import logging

class Note_service:

    logger = logging.getLogger("Note_service")

    def __init__(self, repository: IRepository):
        self.__repository = repository

    def save_note(self, note: Note) -> None:
        note.sanitize()
        note_entity = Mapper.toEntity(note)
        self.__repository.save_note(note_entity)

    def get_note(self, id: int) -> Note:
        try:
            note_entity = self.__repository.get_by_id(id)
            return Mapper.toModel(note_entity)
        except NoteNotFoundException as ex:
            self.logger.error(f"Note with id {id} not found")
            raise NotFoundException(ex) from ex
    
    def get_all_note(self) -> list[Note]:
        note_list = self.__repository.get_all()
        
        return [Mapper.toModel(n_entity) for n_entity in note_list]

    def modify_note(self, note: Note) -> Note:
        try:
            if not self.__repository.exists_by_id(note.id):
                self.logger.error(f"Note with id {note.id} not found")
                raise NotFoundException(NoteNotFoundException(note.id))

            current_note = Mapper.toModel(self.__repository.get_by_id(note.id))
            valid, field, reason = self.__valid_note_to_modify(current_note, note)
            if not valid:
                self.logger.error(f"Note {note.id} is not valid. Invalid field: {field}. Reason: {reason}")
                raise BadNoteException(f"Note {note.id} is not valid. Invalid field: {field}. Reason: {reason}")

            note_modified = self.__repository.modify(Mapper.toEntity(note))
            return Mapper.toModel(note_modified)
        except NoteNotFoundException as ex:
            self.logger.error(f"Note with id {note.id} not found")
            raise NotFoundException(ex) from ex

    def write_content(self, id: int, new_content: str | None) -> int | None:
        try:
            if new_content is not None and Note_validation._MAX_LENGTH_CONTENT < len(new_content):
                self.logger.error("New content length is greater than maximum allowed space")
                raise TextOverflowException("New content length is greater than maximum allowed space")

            note_entity = self.__repository.get_by_id(id)
            if note_entity.completed:
                self.logger.error("Note is closed. It cannot be written")
                raise NonWritableException("Note is closed. It cannot be written")

            if not Note_validation.is_note_writtable(note_entity.content, new_content):
                space_left = Note_validation._MAX_LENGTH_CONTENT - len(note_entity.content)
                return space_left

            updated_content = f"{note_entity.content}\n{new_content}"
            note_entity.content = updated_content
            self.__repository.modify(note_entity)

            return Note_validation._MAX_LENGTH_CONTENT - len(updated_content)

        except NoteNotFoundException as ex:
            self.logger.error(f"Note with id {id} not found")
            raise NotFoundException(ex) from ex

        except DuplicatedNoteException as ex:
            self.logger.error(f"Duplicated note with id {id}")
            raise DuplicationException(ex) from ex

    def get_expired_notes(self) -> list[Note]:
        entity_note_list = self.__repository.get_expired_notes()
        return [Mapper.toModel(entity) for entity in entity_note_list]

    def close_note(self, note_to_complete: Note) -> bool:
        try:
            self.__repository.set_completed(note_to_complete.id, note_to_complete.completed)
            return True
        except NoteNotFoundException as ex:
            self.logger.error(f"Note to complete with id {note_to_complete.id} not found")
            raise NotFoundException(ex) from ex
        except DuplicatedNoteException as ex:
            self.logger.error(f"Duplicated note with id {note_to_complete.id} when trying to complete")
            raise DuplicationException(ex) from ex

    def remove_list_notes(self, note_id_list: list[int]) -> list[int]:
        return [note_id for note_id in note_id_list if Note_validation.is_integer_value(note_id) and self.__repository.remove(note_id)]

    def remove_all(self) -> bool:
        return self.__repository.remove_all()
    
    def __valid_note_to_modify(self, current_note: Note, note_to_modify: Note) -> tuple[bool, str, str]:
        invalid_field = ""
        reason = ""
        valid = True

        if not Note_validation.is_integer_value(note_to_modify.id):
            valid = False
            invalid_field = "id"
            reason = "invalid type"

        if (note_to_modify.deadline_date is not None and
                not Note_validation.valid_date(note_to_modify.deadline_date)):
                valid = False
                invalid_field = "deadline_date"
                reason = "Past date or invalid date format"

        if not Note_validation.is_note_writtable(current_note.content, note_to_modify.content):
            valid = False
            invalid_field = "content"
            reason = "No space left to write"

        return (valid, invalid_field, reason)



