from api.repository.exception.Repository_exception import NoteAlreadyExistsException, NoteNotFoundException
from api.service.mapper.Note_mapper import Mapper
from api.service.model.Model import Note
from api.service.validation.Validations import Note_validation
from ..repository.INote_repository import IRepository
from .exceptions.Service_exception import DuplicationException, NotFoundException, TextOverflowException, NonWritableException

class Note_service:

    def __init__(self, repository: IRepository):
        self.__repository = repository

    def save_note(self, note: Note) -> None:
        try:
            note_entity = Mapper.toEntity(note)
            self.__repository.save_note(note_entity)

        except NoteAlreadyExistsException as ex:
            raise DuplicationException(ex)

    def get_note(self, id: int) -> Note:
        try:
            note_entity = self.__repository.get_by_id(id)
            return Mapper.toModel(note_entity)
        
        except NoteNotFoundException as ex:
            raise NotFoundException(ex)
        
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
            raise NotFoundException(ex)
        
    def get_expired_notes(self) -> list[Note]:
        entity_note_list = self.__repository.get_expired_notes()
        return [Mapper.toModel(entity) for entity in entity_note_list]
    
    def close_notes(self, note_id_list: list[int]) -> bool:
        #TODO: use set_completed repository method
        return False

    def remove_notes(self, note_id_list: list[int]) -> bool:
        # TODO: use remove repository method once implemented
        return False
    

        
    