from pydantic import BaseModel, Field

from src.taskmanager.domain.Model import Note

class NoteResponse(BaseModel):
    id: int | None = Field(..., description = "Note id")
    title: str | None = Field(..., description = "Title of the note")
    content: str | None = Field(..., description = "Content of the note")
    deadline_date: str | None = Field(..., description = "Date of note's expiration")
    completed: bool = Field(..., description = "Indicates if a note is done")
    created_date: str | None = Field(..., description = "Date of note's creation")
    
    @staticmethod
    def to_schema(note: Note):
        return NoteResponse(
            id = note.id,
            title = note.title,
            content = note.content,
            deadline_date=note.deadline_date,
            completed = note.completed,
            created_date=note.created_date
        )
    
class NoteListResponse(BaseModel):
    notes: list[NoteResponse] = Field(default=[], description = "List of notes saved")

    @staticmethod
    def to_schema(note_list: list[Note]):
        return NoteListResponse(notes=[NoteResponse.to_schema(model) for model in note_list])
           