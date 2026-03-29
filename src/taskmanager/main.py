from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

from fastapi import FastAPI
import uvicorn
from src.taskmanager.api.Routers import task_router
from src.taskmanager.api.handler.Exceptions import Exception_handler

app = FastAPI(title="Task Management API", version="1.0.0")
app.include_router(task_router)
Exception_handler(app)

if __name__ == "__main__":
    uvicorn.run("src.taskmanager.main:app", host="0.0.0.0", port=8000, log_level="info")