from fastapi import FastAPI
import uvicorn
from src.taskmanager.api.Routers import task_router
from src.taskmanager.api.handler.Exceptions import Exception_handler

app = FastAPI(title="Task Management API", version="1.0.0")
app.include_router(task_router)
Exception_handler(app)

if __name__ == "__main__":
    uvicorn.run("src.taskmanager.main:app", host="127.0.0.1", port=8080, log_level="info")