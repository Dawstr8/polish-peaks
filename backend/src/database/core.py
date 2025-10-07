from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./polish_peaks.db"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as db:
        yield db


DbSession = Annotated[Session, Depends(get_db)]
