class DuplicationException(Exception):

    def __init__(self, exception: Exception):
        self.__exception = exception

class NotFoundException(Exception):
    def __init__(self, exception: Exception):
        self.__exception = exception

class NonWritableException(Exception):

    def __init__(self, message: str):
        self.__message = message
    
    def get_message(self) -> str:
        return self.__message 

class TextOverflowException(Exception):

    def __init__(self, message: str):
        self.__message = message
    
    def get_message(self) -> str:
        return self.__message