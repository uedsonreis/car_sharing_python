from sqlmodel import SQLModel, Field, Column, VARCHAR


class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password: str = ""


class UserInput(SQLModel):
    username: str
    password: str

class UserOutput(SQLModel):
    id: int
    username: str
