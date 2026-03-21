from datetime import datetime
from typing import Optional, Union

class Note:

    MAX_LENGTH_TITLE = 16
    MAX_LENGTH_CONTENT = 255

    def __init__(self, title: str, content: str, deadline_date: str, id: int | None = None, created_date: str | None = None, updated_date:  str | None = None, completed: bool = False):
        self.__id = id
        self.__title = title
        self.__content = content
        self.__completed = completed
        self.__created_date = created_date
        self.__updated_date = updated_date
        self.__deadline_date = deadline_date

    def sanitize(self) -> None:
        if self.__title is not None:
            self.__title = self.__title.strip()
        if self.__content is not None:
            self.__content = self.__content.strip()

        if not self.__title:
            raise ValueError("Title is required and cannot be empty.")
        if not self.__content:
            raise ValueError("Content is required and cannot be empty.")
        if len(self.__title) > Note.MAX_LENGTH_TITLE:
            raise ValueError(f"Title exceeds maximum allowed length of {Note.MAX_LENGTH_TITLE} characters.")
        if len(self.__content) > Note.MAX_LENGTH_CONTENT:
            raise ValueError(f"Content exceeds maximum allowed length of {Note.MAX_LENGTH_CONTENT} characters.")