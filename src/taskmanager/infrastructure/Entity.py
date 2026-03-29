from types import UnionType
from typing import Tuple

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Index

class Base(DeclarativeBase):
    pass

class Note_entity(Base):
    __tablename__ = "Note"

    id: Mapped[int] = mapped_column(Integer, nullable=True, primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String(16), default = "", nullable = False)
    content: Mapped[str] = mapped_column(String(255), default = "", nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default = False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable = False)
    updated_date: Mapped[datetime | None] = mapped_column(DateTime, default=None, onupdate=datetime.now, nullable=True)
    deadline_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_note_completed", "completed"),
    )

    @staticmethod
    def transform_to_entity(tuple: Tuple):
        return Note_entity(
            id = tuple[0],
            title = tuple[1],
            content = tuple[2],
            completed = tuple[3],
            created_date = tuple[4],
            updated_date = tuple[5],
            deadline_date = tuple[6]
        )