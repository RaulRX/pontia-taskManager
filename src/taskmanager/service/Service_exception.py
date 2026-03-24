class DuplicationException(Exception):

    def __init__(self, exception: Exception):
        super().__init__(exception)

class NotFoundException(Exception):
    def __init__(self, exception: Exception):
        super().__init__(exception)

class BadNoteException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class NonWritableException(Exception):

    def __init__(self, message: str):
        super().__init__(message)

class TextOverflowException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
