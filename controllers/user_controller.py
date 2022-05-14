from fastapi import Depends, APIRouter

from models.user import UserOutput, UserInput, User
from services.user_service import UserService

users = APIRouter(prefix="/users")


@users.post("", response_model=UserOutput)
def store(body: UserInput, service: UserService = Depends(UserService)) -> UserOutput:
    """Stored a new car."""
    user = User.from_orm(body)
    saved = service.create(user)
    return UserOutput.from_orm(saved)
