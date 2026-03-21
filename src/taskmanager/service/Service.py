from src.taskmanager.repository.Repository_exception import DuplicatedNoteException, NoteAlreadyExistsException, NoteNotFoundException
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
        try:
            note.sanitize()
            note_entity = Mapper.toEntity(note)
            self.__repository.save_note(note_entity)

        except NoteAlreadyExistsException as ex:
            raise DuplicationException(ex) from ex

    def get_note(self, id: int) -> Note:
        try:
            note_entity = self.__repository.get_by_id(id)
            return Mapper.toModel(note_entity)

        except NoteNotFoundException as ex:
            raise NotFoundException(ex) from ex

    def modify_note(self, note: Note) -> None:
        
        if not self.__repository.exists_by_id(note.__id):
            raise NotFoundException(NoteNotFoundException(note.__id))

        current_note = Mapper.toModel(self.__repository.get_by_id(note.__id))
        valid, field_list = self.__valid_note_to_modify(current_note, note)
        if not valid:
            raise BadNoteException(f"Note {note.__id} is not valid. Invalid fields: {str(field_list)}")

        self.__repository.modify(Mapper.toEntity(note))    

    def write_content(self, id: int, new_content: str) -> int | None:
        try:
            if Note_validation._MAX_LENGTH_CONTENT < len(new_content):
                raise TextOverflowException("New content lenght is greather than maximun allowed space")

            note_entity = self.__repository.get_by_id(id)
            if note_entity.completed:
                raise NonWritableException("Note is closed. It cannot be writen")

            if not Note_validation.is_note_writtable(note_entity.content, new_content):
                space_left = Note_validation._MAX_LENGTH_CONTENT - len(note_entity.content)
                return space_left

            updated_content = f"{note_entity.content}\\n{new_content}"
            note_entity.content = updated_content
            self.__repository.modify(note_entity)

            return Note_validation._MAX_LENGTH_CONTENT - len(updated_content)

        except NoteNotFoundException as ex:
            raise NotFoundException(ex) from ex

        except DuplicatedNoteException as ex:
            raise DuplicationException(ex) from ex

    def get_expired_notes(self) -> list[Note]:
        entity_note_list = self.__repository.get_expired_notes()
        return [Mapper.toModel(entity) for entity in entity_note_list]

    def close_notes(self, note_id_list: list[int] = []) -> list[int]:
        closed_notes = []

        for note_id in note_id_list:
            if Note_validation.is_integer_value(note_id):
                self.logger.warning(f"Note ID {note_id} is not valid.")
                continue;
            try:
                note = self.__repository.get_by_id(note_id)
                self.__repository.set_completed(note.id)
                closed_notes.append(note_id)

            except NoteNotFoundException as ex:
                self.logger.warning(f"Note ID {note_id} does not exists. It will be skipped.")
            
            except DuplicatedNoteException as ex:
                raise DuplicationException(ex) from ex
        else:
            self.logger.warning("List of notes is empty.")

        return closed_notes

    def remove_list_notes(self, note_id_list: list[int]) -> list[int]:
        return [note_id for note_id in note_id_list if Note_validation.is_integer_value(note_id) and self.__repository.remove(note_id)]

    def remove_all(self) -> bool:
        return self.__repository.remove_all()
    
    def __valid_note_to_modify(self, current_note: Note, note_to_modify: Note) -> tuple[bool, list[str]]:
        invalid_fields = []

        if not Note_validation.is_integer_value(note_to_modify.__id):
            invalid_fields.append("id")

        if note_to_modify.__deadline_date is not None:
            if not Note_validation.valid_date(note_to_modify.__deadline_date):
                invalid_fields.append("deadline_date")

        if not Note_validation.is_note_writtable(current_note.__content, note_to_modify.__content):
            invalid_fields.append("content")

        return (len(invalid_fields) == 0, invalid_fields)



