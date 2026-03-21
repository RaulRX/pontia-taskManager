from pydantic import BaseModel, Field, field_serializer
from datetime import datetime

from src.taskmanager.domain.Model import Note

class TaskResponse(BaseModel):
    id: int | None = Field(..., description = "Note id")
    title: str = Field(..., description = "Title of the note")
    content: str = Field(..., description = "Content of the note")
    deadline_date: str = Field(..., description = "Date of note's expiration")
    completed: bool = Field(..., description = "Indicates if a note is done")
    created_date: str | None = Field(..., description = "Date of note's creation")

    @field_serializer("deadline_date", "created_date")
    def datetime_to_str(self, date: datetime) -> str:
        return date.isoformat()
    
    def to_schema(self, note: Note):
        return TaskResponse(
            id = note.__id,
            title = note.__title,
            content = note.__content,
            deadline_date=note.__deadline_date,
            completed = note.__completed,
            created_date=note.__created_date
        )