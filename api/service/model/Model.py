from datetime import datetime

class Note:

    def __init__(self, title: str, content: str, updated_date = None, deadline_date = None, created_date = None, id = None, completed: bool = False):
        self.__id = id
        self.__title = title
        self.__content = content
        self.__completed = completed
        self.__created_date = created_date
        self.__updated_date = updated_date
        self.__deadline_date = deadline_date