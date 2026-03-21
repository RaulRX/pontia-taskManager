from types import UnionType


class NoteAlreadyExistsException(Exception):

    def __init__(self, title: str):
         super().__init__(f"Active note with title {title} already exists")

class NoteNotFoundException(Exception):

    def __init__(self, id: int | None):
         super().__init__(f"Note with id {id} not found")

class DuplicatedNoteException(Exception):

    def __init__(self, id: int):
         super().__init__(f"Note with id {id} has multiple results")
