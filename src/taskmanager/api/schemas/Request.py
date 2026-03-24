from pydantic import BaseModel, model_validator, Field

from src.taskmanager.domain.Model import Note

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=16, examples=["Mi first note"],
                       description="Título de la nota")
    content: str = Field(..., min_length=1, max_length=255, 
                         examples=["Dear diary, today i was at home when ...."],
                         description="Contenido de la nota")
    deadline: str = Field(..., examples=["2026-03-21", "2026-03-21T15:00:00"],
                          description="Fecha de vencimiento de la nota",
                          pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?)?$")

    @model_validator(mode = "before")
    def remove_spaces(cls, request: dict):
        for key, value in request.items():
           if key not in ['title', 'content', 'deadline']:
               continue
           if not isinstance(value, str):
               raise ValueError("All properties must be strings")
           request[key] = value.strip()
        return request

    def to_model(self) -> Note:
        return Note(
            title = self.title,
            content = self.content,
            deadline_date=self.deadline
        )

class TaskComplete(BaseModel):
    completed: bool = Field(..., description="Estado de completado")

    def to_model(self, id: int | None = None) -> Note:
        return Note(
            id = self.id,
            completed=self.completed
        )

class TaskWriteNote(BaseModel):
    content: str = Field(..., description="Estado de completado", min_length=1, max_length=255)

    @model_validator(mode = "before")
    def remove_spaces(cls, request: dict):
        content = request['content']
        if not isinstance(content, str):
               raise ValueError("Content value must be a string")

        request['content'] = content.strip()
        return request

    def to_model(self, id: int | None = None) -> Note:
        return Note(
            id = id,
            content = self.content
        )

class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=16, examples=["Mi first note"],
                       description="Título de la nota")
    content: str = Field(..., min_length=1, max_length=255, 
                         examples=["Dear diary, today i was at home when ...."],
                         description="Contenido de la nota")
    deadline: str = Field(..., examples=["2026-03-21", "2026-03-21T15:00:00"],
                          description="Fecha de vencimiento de la nota",
                          pattern=r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?)?$")

    @model_validator(mode = "before")
    def remove_spaces(cls, request: dict):
        for key, value in request.items():
           if key in ['title', 'content', 'deadline'] and not isinstance(value, str):
               raise ValueError("All values must be strings")
           request[key] = request[key].strip()
        return request

    def to_model(self, id: int | None = None) -> Note:
        return Note(
            id = id,
            title = self.title,
            content = self.content,
            deadline_date=self.deadline
        )