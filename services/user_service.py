from fastapi import Depends
from passlib.context import CryptContext

from models.user import User
from repositories.user_repository import UserRepository


class UserService:
    bcrypt = CryptContext(schemes=["bcrypt"])
    repository: UserRepository

    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository = repository

    def get(self, username: str):
        return self.repository.get_by_username(username)

    def create(self, user: User):
        user.password = self.bcrypt.hash(user.password)
        return self.repository.create(user)

    def verify_user(self, username: str, password: str):
        user = self.repository.get_by_username(username)
        if user:
            return self.bcrypt.verify(password, user.password)
        return False
