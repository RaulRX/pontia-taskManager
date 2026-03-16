from ..model.Model import Note
from ...repository.entity.Entity import Note_entity


class Mapper:

    @staticmethod
    def toEntity(note: Note) -> Note_entity:
        return Note_entity(
            id = note.__id,
            title = note.__title,
            content = note.__content,
            completed = note.__completed,
            created_date = note.__created_date,
            updated_date = note.__updated_date,
            deadline_date = note.__deadline_date
        )

    @staticmethod
    def toModel(entity: Note_entity) -> Note:
        return Note(
            entity.title,
            entity.content,
            entity.updated_date,
            entity.deadline_date,
            entity.created_date,
            entity.id,
            entity.completed,
        )