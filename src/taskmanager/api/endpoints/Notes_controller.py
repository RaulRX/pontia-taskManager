from fastapi import Response, status
from fastapi import APIRouter
import os
import logging
from src.taskmanager.repository.postgres.Note_repository_impl import Repository
from src.taskmanager.api.schemas.Request import TaskCreate, TaskComplete, TaskUpdate, TaskWriteNote
from src.taskmanager.api.schemas.Response import NoteListResponse, NoteResponse
from src.taskmanager.service.Service import Note_service
from src.taskmanager.infrastructure.Configuration import Postgres_Initializer

logger = logging.getLogger("Notes_controller")

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
            422: {"description": "Validation error — field type mismatch, pattern violation or missing required field"},
        })
def create_note(task: TaskCreate) -> None:
    logger.info("Notes_controller::create_note -> Starting creating note")
    note_service.save_note(task.to_model())
    logger.info("Notes_controller::create_note -> Finished creating note")

@router.get(path="",
        status_code=status.HTTP_200_OK,
        summary="Get all notes created",
        operation_id="get_all_notes",
        response_model=NoteListResponse)
def get_all_notes() -> NoteListResponse:
    logger.info("Notes_controller::get_all_notes -> Starting retrieving all notes")
    notes = note_service.get_all_note()
    response = NoteListResponse.to_schema(notes)
    logger.info("Notes_controller::get_all_notes -> Finished retrieving all notes")
    return response

@router.get(path="/expirationNotes",
        status_code=status.HTTP_200_OK,
        summary="Get all notes that are expired",
        operation_id="get_expired_notes",
        response_model=NoteListResponse)
def get_expired_notes() -> NoteListResponse:
    logger.info("Notes_controller::get_expired_notes -> Starting retrieving expired notes")
    notes = note_service.get_expired_notes()
    response = NoteListResponse.to_schema(notes)
    logger.info("Notes_controller::get_expired_notes -> Finished retrieving expired notes")
    return response

@router.get(path="/{id}",
        status_code=status.HTTP_200_OK,
        summary="Get note by id",
        operation_id="get_note",
        response_model=NoteResponse,
        responses={
            404: {"description": "Note not found"},
        })
def get_note(id: int) -> NoteResponse:
    logger.info("Notes_controller::get_note -> Starting retrieving note by id")
    note = note_service.get_note(id)
    response = NoteResponse.to_schema(note)
    logger.info("Notes_controller::get_note -> Finished retrieving note by id")
    return response

@router.put(path="/{id}",
        status_code=status.HTTP_200_OK,
        summary="Modify note by id",
        operation_id="modify_note",
        response_model=NoteResponse,
        responses={
            404: {"description": "Note not found"},
            422: {"description": "Validation error — invalid date format, content too long, or field type mismatch"},
        })
def modify_note(id: int, note_to_modify: TaskUpdate) -> NoteResponse:
    logger.info("Notes_controller::modify_note -> Starting modifying note")
    note_model = note_to_modify.to_model(id)
    note = note_service.modify_note(note_model)
    response = NoteResponse.to_schema(note)
    logger.info("Notes_controller::modify_note -> Finished modifying note")
    return response

@router.patch(path="/{id}/content",
        status_code=status.HTTP_200_OK,
        summary="Add content to note. I returns space left to write",
        operation_id="modify_note_content",
        response_description="Espacio restante para escribir en la nota",
        responses={
            404: {"description": "Note not found"},
            400: {"description": "New content exceeds maximum allowed length"},
            409: {"description": "Note is closed and cannot be written, or duplicated note found"},
            422: {"description": "Validation error — content must be a non-empty string"},
        })
def modify_note_content(id: int, content_to_modify: TaskWriteNote) -> int | None:
    logger.info("Notes_controller::modify_note_content -> Starting writing content to note")
    note_model = content_to_modify.to_model(id)
    result = note_service.write_content(id, note_model.content)
    logger.info("Notes_controller::modify_note_content -> Finished writing content to note")
    return result

@router.patch(path="/{id}/completed",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Set note to completed",
        operation_id="complete_note",
        response_class=Response,
        responses={
            404: {"description": "Note not found"},
            409: {"description": "Duplicated note found"},
            422: {"description": "Validation error — 'completed' must be a boolean"},
        })
def complete_note(id: int, content_to_modify: TaskComplete) -> None:
    logger.info("Notes_controller::complete_note -> Starting completing note")
    note_model = content_to_modify.to_model(id)
    note_service.close_note(note_model)
    logger.info("Notes_controller::complete_note -> Finished completing note")

@router.delete(path="",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Remove all notes",
        operation_id="remove_notes",
        response_class=Response)
def remove_notes() -> None:
    logger.info("Notes_controller::remove_notes -> Starting removing all notes")
    note_service.remove_all()
    logger.info("Notes_controller::remove_notes -> Finished removing all notes")

@router.delete(path="/{id}",
        status_code=status.HTTP_200_OK,
        summary="Remove note by id",
        operation_id="remove_note",
        response_description="List of IDs successfully removed")
def remove_note(id: int) -> list[int]:
    logger.info("Notes_controller::remove_note -> Starting removing note by id")
    result = note_service.remove_list_notes([id])
    logger.info("Notes_controller::remove_note -> Finished removing note by id")
    return result
