from fastapi import Response, status
from fastapi import APIRouter
import os
from src.taskmanager.repository.postgres.Note_repository_impl import Repository
from src.taskmanager.api.schemas.Request import TaskCreate, TaskComplete, TaskUpdate, TaskWriteNote
from src.taskmanager.api.schemas.Response import NoteListResponse, NoteResponse
from src.taskmanager.service.Service import Note_service
from src.taskmanager.infrastructure.Configuration import Postgres_Initializer

router = APIRouter()
notes_repo = Repository(Postgres_Initializer(os.getenv("POSTGRES_DB_TABLE", "Notes")))
note_service = Note_service(notes_repo)

@router.post(path="",
        status_code=status.HTTP_201_CREATED,
        summary="Create a new note",
        operation_id="create_note",
        response_class=Response,
        responses={
            400: {"description": "Title or content is empty or exceeds maximum allowed length"},
            422: {"description": "Validation error in request body"},
        })
def create_note(task: TaskCreate) -> None:
    note_service.save_note(task.to_model())

@router.get(path="",
        status_code=status.HTTP_200_OK,
        summary="Get all notes created",
        operation_id="get_all_notes",
        response_model=NoteListResponse)
def get_all_notes() -> NoteListResponse:
    notes = note_service.get_all_note()
    return NoteListResponse.to_schema(notes)

@router.get(path="/expirationNotes",
        status_code=status.HTTP_200_OK,
        summary="Get all notes that are expired",
        operation_id="get_expired_notes",
        response_model=NoteListResponse)
def get_expired_notes() -> NoteListResponse:
    notes = note_service.get_expired_notes()
    return NoteListResponse.to_schema(notes)

@router.get(path="/{id}",
        status_code=status.HTTP_200_OK,
        summary="Get note by id",
        operation_id="get_note",
        response_model=NoteResponse,
        responses={
            404: {"description": "Note not found"},
        })
def get_note(id: int) -> NoteResponse:
    note = note_service.get_note(id);
    return NoteResponse.to_schema(note)

@router.put(path="/{id}",
        status_code=status.HTTP_200_OK,
        summary="Modify note by id",
        operation_id="modify_note",
        response_model=NoteResponse,
        responses={
            404: {"description": "Note not found"},
            400: {"description": "Invalid note fields (invalid date format or content too long)"},
        })
def modify_note(id: int, note_to_modify: TaskUpdate) -> NoteResponse:
    note_model = note_to_modify.to_model(id)
    note = note_service.modify_note(note_model)

    return NoteResponse.to_schema(note)

@router.patch(path="/{id}/content",
        status_code=status.HTTP_200_OK,
        summary="Add content to note. I returns space left to write",
        operation_id="modify_note_content",
        response_description="Espacio restante para escribir en la nota",
        responses={
            404: {"description": "Note not found"},
            400: {"description": "New content exceeds maximum allowed length"},
            409: {"description": "Note is closed and cannot be written, or duplicated note found"},
        })
def modify_note_content(id: int, content_to_modify: TaskWriteNote) -> int | None:
    note_model = content_to_modify.to_model(id)
    return note_service.write_content(id, note_model.content)

@router.patch(path="/{id}/completed",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Set note to completed",
        operation_id="complete_note",
        response_class=Response,
        responses={
            404: {"description": "Note not found"},
            409: {"description": "Duplicated note found"},
        })
def complete_note(id: int, content_to_modify: TaskComplete) -> None:
    note_model = content_to_modify.to_model(id)
    note_service.close_note(note_model)

@router.delete(path="",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Remove all notes",
        operation_id="remove_notes",
        response_class=Response)
def remove_notes() -> None:
    note_service.remove_all()

@router.delete(path="/{id}",
        status_code=status.HTTP_200_OK,
        summary="Remove note by id",
        operation_id="remove_note",
        response_description="List of IDs successfully removed")
def remove_note(id: int) -> list[int]:
    return note_service.remove_list_notes([id])