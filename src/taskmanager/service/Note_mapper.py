from src.taskmanager.domain.Model import Note
from src.taskmanager.infrastructure.Entity import Note_entity
from datetime import datetime

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
            datetime.isoformat(entity.deadline_date),
            entity.id,
            datetime.isoformat(entity.created_date),
            datetime.isoformat(entity.updated_date),
            entity.completed
        )
