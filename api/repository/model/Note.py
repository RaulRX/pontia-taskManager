from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Index

from ..config.Configuration import Initializer

class Base(DeclarativeBase):
    pass

class Note:
    __tablename__ = "Notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String(16), nullable= False)
    content: Mapped[str] = mapped_column(String(255), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable = False)
    updated_date: Mapped[datetime] = mapped_column(DateTime, default=None, onupdate=datetime.now())
    deadline_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_note_completed", "completed", sqlite_where="completed = 1"),
        CheckConstraint("length(trim(title)) > 0", name="ck_notes_title_not_blank")
    )