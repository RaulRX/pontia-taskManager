from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Initializer:

    _BASE_DIR = Path(__file__).parent
    _DATABASE_PREFIX = "sqlite:///"
    _LOGGIN_PREFIX = "SqlAlchemy"
    _LOGGIN_SUFFIX = "Repo"

    def __init__(self, database_path: str):
        self.__engine = create_engine(
            f"{self._DATABASE_PREFIX}{self._BASE_DIR / 'data' / database_path}",
            connect_args={"check_same_thread": False},
            hide_parameters=True,
            logging_name=f"{self._LOGGIN_PREFIX}_{database_path.removesuffix('.db')}_{self._LOGGIN_SUFFIX}",
        )
        self.__session = sessionmaker(bind=self.__engine, autocommit=False, autoflush=False)

    def get_session(self):
        return self.__session()

    def create_tables(self, base: type[DeclarativeBase]):
        base.metadata.create_all(self.__engine)
