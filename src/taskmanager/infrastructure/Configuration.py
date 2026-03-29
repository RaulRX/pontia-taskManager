from abc import abstractmethod
from pathlib import Path
import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.taskmanager.infrastructure.data import Query

BASE_DIR = Path(__file__).parent

class Db_initializer:

    def __init__(self, database_path: str):
        self._database_path = f"{BASE_DIR / 'data' / database_path}"

    @abstractmethod
    def get_connection(self):
        raise NotImplementedError()
    
    @abstractmethod
    def get_session(self):
        raise NotImplementedError()
    
    @abstractmethod
    def create_tables(self) -> None:
        raise NotImplementedError()

    
class SqlLite_Initializer(Db_initializer):

    def __init__(self, database_path: str):
        
        super().__init__(database_path)
        DATABASE_PREFIX = os.getenv("SQLITE_HOST", "sqlite:///")
        LOGGIN_PREFIX = "SqlAlchemy"
        LOGGIN_SUFFIX = "Repo"
        
        self.__engine = create_engine(
            f"{DATABASE_PREFIX}{self._database_path}",
            connect_args={"check_same_thread": False},
            hide_parameters=True,
            logging_name=f"{LOGGIN_PREFIX}_{database_path.removesuffix('.db')}_{LOGGIN_SUFFIX}",
        )
        self.__session = None

    def get_session(self):
        if self.__session is not None:
            return self.__session()
        
        self.__session = sessionmaker(bind=self.__engine, autocommit=False, autoflush=False)
        return self.__session

    def create_tables(self) -> None:
        DeclarativeBase.metadata.create_all(self.__engine)

    def get_connection(self):
        return self.__engine

class Postgres_Initializer(Db_initializer):

    def __init__(self, database_path: str):
        super().__init__(database_path)
        HOST = os.getenv("POSTGRES_HOST")
        USER = os.getenv("POSTGRES_USER")
        PASSWORD = os.getenv("POSTGRES_PASSWORD")
        PORT = os.getenv("POSTGRES_PORT")
        DB = os.getenv("POSTGRES_DB")
        self.__connection = psycopg2.connect(
            database=DB,
            host=HOST,
            user=USER,
            password=PASSWORD,
            port=PORT
        )

        self.__session = None
        
    def get_session(self):
        if self.__session is not None:
            self.__session
        
        self.__session = self.__connection.cursor()
        return self.__connection.cursor()

    def create_tables(self):
        pass
    
    def get_connection(self):
        return self.__connection
