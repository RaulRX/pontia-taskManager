from fastapi import status
from src.taskmanager.api.Routers import APIRouter
from src.taskmanager.api.schemas.Request import TaskCreate
from src.taskmanager.service.Service import Note_service
from src.taskmanager.repository.Note_repository_impl import Repository
from src.taskmanager.infrastructure.Configuration import Initializer

router = APIRouter()
# Inicializar base de datos y repositorio
notes_repo = Repository(Initializer("notes.db"))
note_service = Note_service(notes_repo)

@router.post(path="/messages",
        status_code=status.HTTP_201_CREATE,
        summary="",
        operation_id="create_note")
def create_note(task: TaskCreate):
    model = task.to_model()
    note_service.save_note(model)

# @router.get("/{task_id}", response_model=TaskResponse)
# def obtener_tarea(task_id: int):
#     ...

# @router.put("/{task_id}/completar", response_model=TaskResponse)
# def marcar_completada(task_id: int):
#     ...

# @router.get("/caducadas", response_model=List[TaskResponse])
# def obtener_tareas_caducadas():
#     ...