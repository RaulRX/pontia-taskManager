class NoteNotFoundException(Exception):

    def __init__(self, id: int | None):
         super().__init__(f"Note with id {id} not found")

class DuplicatedNoteException(Exception):

    def __init__(self, id: int):
         super().__init__(f"Note with id {id} has multiple results")

class MultipleResultsFound(Exception):
     def __init__(self):
         super().__init__(f"Multiple results where found")