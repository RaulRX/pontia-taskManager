from fastapi import APIRouter
from src.taskmanager.api.endpoints import Notes_controller

task_router = APIRouter()
task_router.include_router(Notes_controller.router, prefix="/tasks", tags=["tasks"])