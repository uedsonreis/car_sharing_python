from sqlalchemy.engine import Engine
from sqlmodel import create_engine, SQLModel, Session


engine: Engine = create_engine(
    "sqlite:///carsharing.db",
    connect_args={"check_same_thread": False},
    echo=True  # Log generated SQL
)


def init_session():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
