from http import HTTPStatus
from urllib import response

from fastapi import Response, status
from starlette.status import HTTP_200_OK
from fastapi import APIRouter
from src.taskmanager.api.schemas.Request import TaskCreate, TaskUpdate, TaskWriteNote
from src.taskmanager.api.schemas.Response import NoteListResponse, NoteResponse
from src.taskmanager.service.Service import Note_service
from src.taskmanager.repository.Note_repository_impl import Repository
from src.taskmanager.infrastructure.Configuration import Initializer

router = APIRouter()
# Inicializar base de datos y repositorio
notes_repo = Repository(Initializer("notes.db"))
note_service = Note_service(notes_repo)

@router.post(path="",
        status_code=status.HTTP_201_CREATED,
        summary="Create a new note",
        operation_id="create_note", 
        response_class=Response)
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

@router.get(path="/{id}",
        status_code=status.HTTP_200_OK,
        summary="Get note by id",
        operation_id="get_note",
        response_model=NoteResponse)
def get_note(id: int) -> NoteResponse:
    note = note_service.get_note(id);
    return NoteResponse.to_schema(note)

@router.put(path="/{id}",
        status_code=status.HTTP_200_OK,
        summary="Modify note by id",
        operation_id="modify_note",
        response_model=NoteResponse)
def modify_note(id: int, note_to_modify: TaskUpdate) -> NoteResponse:
    note_model = note_to_modify.to_model(id)
    note = note_service.modify_note(note_model)

    return NoteResponse.to_schema(note)

@router.patch(path="/{id}",
        status_code=status.HTTP_200_OK,
        summary="Add content to note",
        operation_id="modify_note_content")
def modify_note_content(id: int, content_to_modify: TaskWriteNote) -> NoteResponse:
    note_model = content_to_modify.to_model(id)
    note = note_service.modify_note(note_model)

    return NoteResponse.to_schema(note)


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