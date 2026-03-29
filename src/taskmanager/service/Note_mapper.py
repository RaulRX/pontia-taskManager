from src.taskmanager.domain.Model import Note
from src.taskmanager.infrastructure.Entity import Note_entity
from datetime import datetime

class Mapper:

    @staticmethod
    def _parse_date(value: str | None) -> datetime | None:
        return datetime.fromisoformat(value) if value else None

    @staticmethod
    def toEntity(note: Note) -> Note_entity:
        entity = Note_entity(
            id = note.id,
            title = note.title,
            content = note.content,
            completed = note.completed,
            deadline_date = Mapper._parse_date(note.deadline_date),
        )
        if note.created_date:
            entity.created_date = datetime.fromisoformat(note.created_date)
        if note.updated_date:
            entity.updated_date = datetime.fromisoformat(note.updated_date)
        return entity

    @staticmethod
    def _format_date(value: datetime | None) -> str | None:
        return value.isoformat() if value is not None else None

    @staticmethod
    def toModel(entity: Note_entity) -> Note:
        print(entity)
        return Note(
            title = entity.title,
            content = entity.content,
            deadline_date = Mapper._format_date(entity.deadline_date),
            id = entity.id,
            created_date = Mapper._format_date(entity.created_date),
            updated_date = Mapper._format_date(entity.updated_date),
            completed = entity.completed,
        )
