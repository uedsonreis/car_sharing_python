from fastapi import Depends
from sqlmodel import Session, select

from models.user import User
from repositories.schemas import get_session


class UserRepository:

    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        return self.session.exec(query).first()

    def create(self, user: User):
        self.session.add(user)

        self.session.commit()
        self.session.refresh(user)
        return user
